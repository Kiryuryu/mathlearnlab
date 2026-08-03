"""Tests for grading prompts — no network, no database."""

from server.services.prompts import GRADER_SYSTEM_PROMPT, build_grading_message


def test_system_prompt_mentions_json_and_chinese():
    assert "JSON" in GRADER_SYSTEM_PROMPT
    assert "verdict" in GRADER_SYSTEM_PROMPT


def test_build_grading_message_has_problem_and_image():
    problem = {
        "problem_statement": "求极限",
        "solution": {"steps": ["step1"], "final_answer": "3", "method": "m"},
        "grading_rubric": {"key_steps": ["k1"], "common_errors": ["e1"]},
    }
    msgs = build_grading_message(problem, "BASE64DATA")
    assert len(msgs) == 2
    assert msgs[0]["type"] == "text"
    assert "求极限" in msgs[0]["text"]
    assert msgs[1]["type"] == "image"
    assert msgs[1]["source"]["data"] == "BASE64DATA"


def test_build_grading_message_empty_rubric():
    problem = {"problem_statement": "x", "solution": {}, "grading_rubric": {}}
    msgs = build_grading_message(problem, "D")
    assert "Student" in msgs[0]["text"]
