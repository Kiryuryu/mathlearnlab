"""Tests for practice service — no network, no database."""

import pytest
from server.services.practice_service import extract_json, build_generate_prompt, DIFF_GUIDE


def test_extract_json_plain():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_extract_json_with_fence():
    raw = '```json\n{"a": 2}\n```'
    assert extract_json(raw) == {"a": 2}


def test_extract_json_with_json_fence():
    raw = '```json\n{"b": 3}\n```'
    assert extract_json(raw) == {"b": 3}


def test_extract_json_salvage_truncated():
    # Trailing garbage after the closing brace — should be salvaged
    raw = '{"c": 4} some trailing text'
    assert extract_json(raw) == {"c": 4}


def test_extract_json_raises_on_invalid():
    with pytest.raises(Exception):
        extract_json("not json at all")


def test_build_prompt_contains_key_fields():
    p = build_generate_prompt("极限", "exam", "极限的严格定义", "GEN-ABC12", "")
    assert "极限" in p
    assert "GEN-ABC12" in p
    assert "problem_statement" in p


def test_diff_guide_covers_levels():
    for k in ["basic", "advanced", "exam", "graduate", "phd"]:
        assert k in DIFF_GUIDE
