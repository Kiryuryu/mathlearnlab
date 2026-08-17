"""
Practice service — AI problem generation helpers (history, prompt, JSON parsing).
Pure helpers so the router stays thin and the logic is testable.

Storage of generated problems/history lives in server.models.problems
(SQLite-backed; race-safe). This module only builds prompts and parses output.
"""

import json

from server.models.problems import load_recent_history, persist_problem, record_generated


def build_recent_avoidance(topic_key: str) -> str:
    """Text listing recently generated problems so the AI avoids duplicates."""
    recent = [h.get("preview", "") for h in load_recent_history(topic_key, 10) if h.get("preview")]
    if not recent:
        return ""
    return (
        "\n\n以下是最近生成过的题目，请勿重复或高度相似，换一个角度或知识点：\n"
        + "\n".join(f"- {r}" for r in recent)
    )


DIFF_GUIDE = {
    "basic": "基础入门题，考察核心概念的直观理解，适合刚学完概念的学生",
    "advanced": "进阶提高题，需要综合运用多个知识点，有适度的技巧性",
    "exam": "考研难度，综合性强，需要灵活运用概念和技巧，对应数学一/二/三难度",
    "graduate": "研究生水平，需要深刻理解概念本质，可能涉及证明或构造性思维",
    "phd": "博士级难度，需要高度创造性的数学思维，可能是开放性问题或需要构造反例",
}


def build_generate_prompt(exhibit_name: str, difficulty: str, knowledge_points: str, gen_id: str, avoid_text: str) -> str:
    return f"""你是一位数学命题专家。请为"{exhibit_name}"主题生成一道练习题。

难度级别：{difficulty}
难度要求：{DIFF_GUIDE.get(difficulty, "中等难度")}
相关知识点：{knowledge_points}
{avoid_text}

请用 JSON 格式输出：
{{
  "id": "{gen_id}",
  "difficulty": "{difficulty}",
  "knowledge_points": ["知识点1", "知识点2"],
  "problem_statement": "完整的题目描述，用 LaTeX 语法写数学公式",
  "preview": "题目简短预览（120字以内）",
  "solution": {{
    "method": "解题思路概述",
    "steps": ["步骤1的详细描述", "步骤2的详细描述", "步骤3的详细描述"],
    "final_answer": "最终答案，LaTeX 格式"
  }},
  "grading_rubric": {{
    "key_steps": ["关键得分步骤1", "关键得分步骤2"],
    "common_errors": ["常见错误1", "常见错误2"]
  }},
  "metadata": {{"problem_type": "计算题"}}
}}

只输出 JSON，不要其他内容。确保 problem_statement 使用正确的 LaTeX 语法（$...$ 或 $$...$$）。"""


def extract_json(raw: str) -> dict:
    """Parse AI JSON output robustly.

    Strategies in order:
      1. strip ```json fences
      2. try json.loads directly
      3. extract substring from first '{' to last '}'
    """
    text = str(raw)
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to salvage: take first '{' to last '}'
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = text[start:end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                raise
        raise
