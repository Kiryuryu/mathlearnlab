"""Tests for the knowledge graph API and related-field metadata."""

import re
from pathlib import Path

from server.routers import graph as graph_router
from server.content_data import subjects, exhibits

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"


def test_every_parented_exhibit_has_related():
    for key, ex in exhibits.items():
        if not ex.get("parent"):
            continue
        related = ex.get("related")
        assert related, f"{key} missing related"
        assert len(related) > 0, f"{key} has empty related"
        assert key not in related, f"{key} related to itself"
        for target in related:
            assert target in exhibits, f"{key} related to unknown exhibit {target}"


def test_build_graph_shape():
    g = graph_router.build_graph(subjects, exhibits)
    subject_count = sum(1 for n in g["nodes"] if n["type"] == "subject")
    concept_count = sum(1 for n in g["nodes"] if n["type"] == "concept")
    assert subject_count == len(subjects)
    assert concept_count == sum(1 for ex in exhibits.values() if ex.get("parent"))
    parent_edges = [e for e in g["edges"] if e["type"] == "parent"]
    assert len(parent_edges) == concept_count
    for n in g["nodes"]:
        assert n["accent"], f"node {n['id']} missing accent"
    for e in g["edges"]:
        ids = {n["id"] for n in g["nodes"]}
        assert e["source"] in ids and e["target"] in ids


def test_graph_route():
    from fastapi.testclient import TestClient
    from server.main import app
    client = TestClient(app)
    r = client.get("/api/graph")
    assert r.status_code == 200
    data = r.json()
    assert "nodes" in data and "edges" in data
    assert len(data["nodes"]) > 0


def test_related_matches_concept_md():
    """The concept.md 'continue reading' links must be within each exhibit's related."""
    for key, ex in exhibits.items():
        if not ex.get("parent"):
            continue
        concept_md = CONTENT_DIR / "exhibits" / key / "concept.md"
        if not concept_md.exists():
            continue
        text = concept_md.read_text(encoding="utf-8")
        links = set(re.findall(r"\[[^\]]*\]\(/exhibit/([a-z-]+)\)", text))
        related = set(ex.get("related", []) or [])
        for link in links:
            assert link in related, f"{key} concept.md links to {link} not in related {related}"
