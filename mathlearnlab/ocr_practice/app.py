"""
MathLearnLab — OCR 刷题

Streamlit 首页：选题 + API Key 管理 + 答题统计
"""

import streamlit as st

# MUST be the first Streamlit command
st.set_page_config(
    page_title="MathLearnLab — OCR 刷题",
    page_icon="🧮",
    layout="wide",
)

from ocr_practice.pages.page_base import inject_mathjax
from ocr_practice.config import TOPICS
from ocr_practice.utils import problem_loader, history

inject_mathjax()

# ── Header ──
st.title("🧮 MathLearnLab — OCR 刷题")
st.caption("拍照上传手写答案，AI 自动批改并给出详细反馈")

st.divider()

# ── API Key ──
with st.expander("🔑 设置 Anthropic API Key", expanded=False):
    # Try to load from secrets
    try:
        secret_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if secret_key and secret_key != "your-api-key-here":
            st.success("✅ 已从 secrets.toml 加载 API Key")
            api_key = secret_key
        else:
            api_key = ""
    except Exception:
        api_key = ""

    user_key = st.text_input(
        "输入你的 Anthropic API Key",
        type="password",
        value=api_key,
        placeholder="sk-ant-...",
        help="你的 API Key 只保存在当前会话中，不会上传到任何地方。"
    )
    if user_key:
        st.session_state["api_key"] = user_key
        st.success("✅ API Key 已设置")

    st.markdown("""
    > 💡 **没有 API Key？** 前往 [Anthropic Console](https://console.anthropic.com/) 注册并获取。
    每次批改大约消耗 2000 tokens，费用约 \\$0.02。
    """)

st.divider()

# ── Topic Selector ──
st.subheader("📚 选择刷题科目")

# Stats
stats = history.get_stats()

cols = st.columns(len(TOPICS))
for i, (topic_key, topic) in enumerate(TOPICS.items()):
    with cols[i]:
        count = problem_loader.count_problems(topic_key)
        ts = stats.get("by_topic", {}).get(topic_key, {})
        topic_total = ts.get("total", 0)
        topic_correct = ts.get("correct", 0)
        topic_acc = f"{topic_correct}/{topic_total}" if topic_total > 0 else "暂无记录"

        with st.container(border=True):
            st.markdown(f"### {topic['icon']}")
            st.markdown(f"**{topic['zh']}**")
            st.caption(topic['description'])
            st.caption(f"📝 {count} 道题 | 🎯 {topic_acc}")

            if st.button("开始刷题 ➤", key=f"start_{topic_key}",
                         use_container_width=True, type="primary"):
                st.switch_page(f"pages/{i+1:02d}_{topic_key}.py")

st.divider()

# ── Overall Stats ──
st.subheader("📊 答题统计")
if stats["total"] > 0:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("总答题数", stats["total"])
    with col2:
        st.metric("正确率", f"{stats['accuracy']}%")
    with col3:
        st.metric("✅ 正确", stats["correct"])
    with col4:
        st.metric("⚠️ 部分正确", stats["partial"])
    with col5:
        st.metric("❌ 错误", stats["incorrect"])

    # Recent attempts
    with st.expander("📜 最近答题记录"):
        recent = history.get_recent_attempts(10)
        for r in recent:
            v_icon = {"correct": "✅", "partially_correct": "⚠️", "incorrect": "❌"}.get(
                r.get("verdict", ""), "❓"
            )
            topic_name = TOPICS.get(r.get("topic_key", ""), {}).get("zh", "")
            st.markdown(
                f"{v_icon} **{r.get('problem_id', '')}** ({topic_name}) "
                f"— {r.get('score', '')} "
                f"_{r.get('timestamp', '')[:16]}_"
            )
else:
    st.info("👆 选择上面的科目开始刷题吧！")

st.divider()
st.caption("💡 **使用方式**：选题 → 纸笔作答 → 拍照上传 → AI 批改 → 查看反馈 → 错题自动记入错题本")
