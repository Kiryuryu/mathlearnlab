"""
Shared layout and utilities for all OCR practice topic pages.

Each topic page imports this module and calls the appropriate functions
with topic-specific configuration.
"""

import streamlit as st
from ocr_practice.config import TOPICS, DIFFICULTY
from ocr_practice.utils import problem_loader, history, api_client, image_utils


def inject_mathjax():
    """Inject MathJax v3 for LaTeX rendering in st.markdown()."""
    st.components.html("""
    <script>
    window.MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\(', '\\)']],
            displayMath: [['$$', '$$'], ['\\[', '\\]']],
            processEscapes: true,
        },
        svg: {fontCache: 'global'},
        options: {
            skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
        }
    };
    </script>
    <script id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
    </script>
    <script>
    // Re-render MathJax after Streamlit updates
    var observer = new MutationObserver(function() {
        if (window.MathJax && window.MathJax.typesetPromise) {
            MathJax.typesetPromise();
        }
    });
    observer.observe(document.body, {childList: true, subtree: true});
    </script>
    """, height=0)


def get_api_key() -> str | None:
    """Get the API key from Streamlit secrets or session state."""
    # Try secrets first
    try:
        key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if key and key != "your-api-key-here":
            return key
    except Exception:
        pass

    # Fall back to session state
    return st.session_state.get("api_key", None)


def init_page_state(topic_key: str):
    """Initialize session state for a topic page.

    Call this at the start of every topic page.
    """
    defaults = {
        f"{topic_key}_phase": "problem",     # problem | upload | results
        f"{topic_key}_problem": None,         # current problem dict
        f"{topic_key}_image": None,           # uploaded image bytes
        f"{topic_key}_result": None,          # grading result dict
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def render_problem_phase(topic_key: str):
    """Phase 1: Show problem, let user pick random or select from list."""
    topic = TOPICS[topic_key]
    st.subheader(f"{topic['icon']} {topic['zh']} — 刷题")

    # Pick random problem button
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🎲 随机抽题", use_container_width=True, type="primary"):
            problem = problem_loader.get_random_problem(topic_key)
            if problem:
                st.session_state[f"{topic_key}_problem"] = problem
                st.session_state[f"{topic_key}_phase"] = "solve"
                st.session_state[f"{topic_key}_image"] = None
                st.session_state[f"{topic_key}_result"] = None
                st.rerun()
            else:
                st.error("题库为空！请先生成题目。")

    with col2:
        # Difficulty filter dropdown
        diff_filter = st.selectbox(
            "筛选难度", ["全部", "简单", "中等", "困难"],
            key=f"{topic_key}_diff_filter"
        )

    # Problem list
    summaries = problem_loader.list_problem_summaries(topic_key)
    if not summaries:
        st.warning("📭 该 topic 暂无题目。运行 `scripts/seed_problem_bank.py` 生成题目。")
        return

    # Filter
    if diff_filter != "全部":
        summaries = [s for s in summaries if s.get("difficulty") == diff_filter]

    st.caption(f"共 {len(summaries)} 道题")

    for s in summaries:
        d = DIFFICULTY.get(
            {"简单": "easy", "中等": "medium", "困难": "hard"}.get(s["difficulty"], "medium"),
            {},
        )
        tags = " · ".join(s.get("knowledge_points", [])[:3])
        col1, col2 = st.columns([4, 1])
        with col1:
            btn_label = f"{d.get('stars', '')} {s['id']} — {s['preview']}"
            if st.button(btn_label, key=f"pick_{s['id']}", use_container_width=True):
                problem = problem_loader.get_problem(topic_key, s["id"])
                if problem:
                    st.session_state[f"{topic_key}_problem"] = problem
                    st.session_state[f"{topic_key}_phase"] = "solve"
                    st.session_state[f"{topic_key}_image"] = None
                    st.session_state[f"{topic_key}_result"] = None
                    st.rerun()
        with col2:
            st.caption(f"{d.get('zh', '')}")


def render_solve_phase(topic_key: str):
    """Phase 2: Show problem details + upload answer."""
    topic = TOPICS[topic_key]
    problem = st.session_state.get(f"{topic_key}_problem")

    if problem is None:
        st.session_state[f"{topic_key}_phase"] = "problem"
        st.rerun()
        return

    # Back button
    if st.button("← 返回选题"):
        st.session_state[f"{topic_key}_phase"] = "problem"
        st.rerun()

    d = DIFFICULTY.get(problem.get("difficulty", "medium"), {})
    st.subheader(f"{topic['icon']} {problem.get('id', '')}")

    # Metadata
    cols = st.columns(3)
    with cols[0]:
        st.caption(f"难度：{d.get('stars', '')} {d.get('zh', '')}")
    with cols[1]:
        st.caption(f"类型：{problem.get('metadata', {}).get('problem_type', '计算题')}")
    with cols[2]:
        pts = problem.get("knowledge_points", [])
        st.caption(f"知识点：{' · '.join(pts[:2])}{'...' if len(pts) > 2 else ''}")

    # Problem statement
    st.markdown("### 📝 题目")
    st.markdown(problem.get("problem_statement", ""))

    # MathJax re-render
    st.components.html("""
    <script>
    if (window.MathJax) { MathJax.typesetPromise(); }
    </script>
    """, height=0)

    st.divider()

    # Upload
    st.markdown("### 📸 上传你的手写答案")

    col1, col2 = st.columns(2)
    image_bytes = None

    with col1:
        camera_img = st.camera_input("📷 拍照上传", key=f"{topic_key}_camera")
        if camera_img:
            image_bytes = camera_img.getvalue()

    with col2:
        file_img = st.file_uploader("📁 选择图片文件", type=["jpg", "jpeg", "png"],
                                    key=f"{topic_key}_uploader")
        if file_img:
            image_bytes = file_img.getvalue()

    # Show preview
    if image_bytes:
        st.image(image_bytes, caption="上传的答案", width=400)

    # Submit for grading
    st.divider()
    api_key = get_api_key()

    if not api_key:
        st.warning("⚠️ 请先在首页设置 Anthropic API Key")
        if st.button("🏠 回到首页设置"):
            st.switch_page("app.py")
        return

    if st.button("🎯 提交批改", type="primary", use_container_width=True,
                 disabled=(image_bytes is None)):
        if image_bytes is None:
            st.error("请先上传答案图片")
            return

        with st.spinner("🤖 正在识别手写答案并批改... (预计 3-5 秒)"):
            try:
                # Compress image if needed
                img_bytes = image_utils.compress_image(image_bytes)

                # Call Claude for grading
                result = api_client.grade_submission(problem, img_bytes, api_key)

                st.session_state[f"{topic_key}_image"] = image_bytes
                st.session_state[f"{topic_key}_result"] = result
                st.session_state[f"{topic_key}_phase"] = "results"

                # Save to history
                history.save_grade(
                    topic_key=topic_key,
                    problem_id=problem.get("id", ""),
                    problem_statement=problem.get("problem_statement", ""),
                    solution_steps=problem.get("solution", {}).get("steps", []),
                    final_answer=problem.get("solution", {}).get("final_answer", ""),
                    grading_result=result,
                    image_bytes=image_bytes if result.get("verdict") != "correct" else None,
                )

                st.rerun()
            except Exception as e:
                st.error(f"❌ 批改失败：{str(e)}")
                st.info("💡 请检查 API Key 是否正确，网络是否畅通。")


def render_results_phase(topic_key: str):
    """Phase 3: Show grading results."""
    topic = TOPICS[topic_key]
    problem = st.session_state.get(f"{topic_key}_problem")
    result = st.session_state.get(f"{topic_key}_result")

    if problem is None or result is None:
        st.session_state[f"{topic_key}_phase"] = "problem"
        st.rerun()
        return

    # Verdict display
    verdict = result.get("verdict", "unknown")
    verdict_config = {
        "correct": ("✅ 回答正确！", "green"),
        "partially_correct": ("⚠️ 部分正确", "orange"),
        "incorrect": ("❌ 回答错误", "red"),
        "unknown": ("❓ 无法判定", "gray"),
    }
    v_text, v_color = verdict_config.get(verdict, verdict_config["unknown"])

    st.subheader(f"{topic['icon']} {problem.get('id', '')} — 批改结果")
    st.markdown(f"### {v_text}")
    st.caption(f"得分：{result.get('score', '')}")

    st.divider()

    # OCR text
    ocr_text = result.get("ocr_text", "")
    if ocr_text:
        st.markdown("#### 📖 识别到的作答内容")
        st.info(ocr_text)

    # Feedback
    what_correct = result.get("what_is_correct", "")
    what_wrong = result.get("what_is_wrong", "")
    suggestion = result.get("suggestion", "")
    misconception = result.get("key_misconception")

    if what_correct:
        with st.expander("✅ 做得好的地方", expanded=True):
            st.success(what_correct)

    if what_wrong:
        with st.expander("❌ 存在问题", expanded=True):
            st.error(what_wrong)

    if misconception:
        with st.expander("🔍 可能的概念误解"):
            st.warning(misconception)

    if suggestion:
        with st.expander("💡 改进建议"):
            st.info(suggestion)

    # Graded steps (if available)
    graded_steps = result.get("graded_steps", [])
    if graded_steps:
        st.markdown("#### 📋 步骤批改详情")
        for gs in graded_steps:
            status_icon = {"ok": "✅", "wrong": "❌", "missing": "⬜"}.get(
                gs.get("status", ""), "❓"
            )
            st.markdown(f"{status_icon} **{gs.get('step', '')}** — {gs.get('comment', '')}")

    st.divider()

    # Correct solution
    with st.expander("📐 查看标准解答", expanded=(verdict != "correct")):
        st.markdown("**解题方法：** " + problem.get("solution", {}).get("method", ""))
        steps = problem.get("solution", {}).get("steps", [])
        for i, step in enumerate(steps, 1):
            st.markdown(f"{i}. {step}")
        final = problem.get("solution", {}).get("final_answer", "")
        if final:
            st.markdown(f"**最终答案：** {final}")

    st.divider()

    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 再做一题", use_container_width=True, type="primary"):
            st.session_state[f"{topic_key}_phase"] = "problem"
            st.session_state[f"{topic_key}_problem"] = None
            st.session_state[f"{topic_key}_image"] = None
            st.session_state[f"{topic_key}_result"] = None
            st.rerun()

    with col2:
        if st.button("🔁 重做此题", use_container_width=True):
            st.session_state[f"{topic_key}_phase"] = "solve"
            st.session_state[f"{topic_key}_image"] = None
            st.session_state[f"{topic_key}_result"] = None
            st.rerun()

    with col3:
        if verdict in ("incorrect", "partially_correct"):
            if st.button("📝 加入错题本", use_container_width=True):
                _save_to_error_log(problem, result, topic_key)
                st.success("✅ 已加入错题本！")
                st.balloons()


def _save_to_error_log(problem: dict, result: dict, topic_key: str):
    """Append an incorrect problem to the error log markdown."""
    from datetime import datetime, timezone, timedelta
    CST = timezone(timedelta(hours=8))

    error_log_path = f"error-log/01-gaoshu-errors.md"  # relative to project root

    now = datetime.now(CST).strftime("%Y-%m-%d %H:%M")
    problem_id = problem.get("id", "?")
    problem_text = problem.get("problem_statement", "")
    solution_steps = problem.get("solution", {}).get("steps", [])
    final_answer = problem.get("solution", {}).get("final_answer", "")
    what_wrong = result.get("what_is_wrong", "")
    suggestion = result.get("suggestion", "")
    misconception = result.get("key_misconception", "")

    entry = f"""
---
编号: {problem_id}
日期: {now}
来源: OCR刷题
题型: 计算题
知识点: {', '.join(problem.get('knowledge_points', []))}

### 题目
{problem_text}

### 错误原因
{what_wrong}

### 概念误解
{misconception if misconception else '无'}

### 改进建议
{suggestion}

### 正确答案
{chr(10).join(f'{i+1}. {s}' for i, s in enumerate(solution_steps))}
最终答案：{final_answer}

### 教训
{suggestion[:100] if suggestion else '复习相关知识点'}
"""

    try:
        with open(error_log_path, "a", encoding="utf-8") as f:
            f.write(entry)
    except FileNotFoundError:
        # Try absolute path
        import os
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        abs_path = os.path.join(base, error_log_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "a", encoding="utf-8") as f:
            f.write(entry)


def run_topic_page(topic_key: str):
    """Main entry point for any topic page.

    Call this at the bottom of each page file, e.g.:
        from ocr_practice.pages.page_base import run_topic_page
        run_topic_page("integrals")
    """
    # Page config
    topic = TOPICS[topic_key]

    st.set_page_config(
        page_title=f"OCR刷题 — {topic['zh']}",
        page_icon=topic["icon"],
        layout="wide",
    )

    inject_mathjax()
    init_page_state(topic_key)

    phase = st.session_state.get(f"{topic_key}_phase", "problem")

    if phase == "problem":
        render_problem_phase(topic_key)
    elif phase == "solve":
        render_solve_phase(topic_key)
    elif phase == "results":
        render_results_phase(topic_key)
