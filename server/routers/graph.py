"""
Knowledge graph API — subjects and exhibits as nodes, parent/related as edges.
Built from static content_data; no AI involved.
"""

from fastapi import APIRouter
from server.config import settings

router = APIRouter()


def build_graph(subjects: dict, exhibits: dict) -> dict:
    """Return {nodes, edges} for the knowledge graph.

    Nodes: 7 subjects + parented exhibits (concepts).
    Edges: parent (subject→concept) + related (concept→concept, undirected, deduped).
    """
    nodes = []
    edges = []
    concept_keys = set()

    for key, s in subjects.items():
        nodes.append({
            "id": key,
            "type": "subject",
            "zh": s.get("zh", ""),
            "en": s.get("en", ""),
            "icon": s.get("icon", ""),
            "accent": s.get("accent", ""),
        })

    for key, ex in exhibits.items():
        if not ex.get("parent"):
            continue
        concept_keys.add(key)
        parent = ex.get("parent")
        nodes.append({
            "id": key,
            "type": "concept",
            "parent": parent,
            "zh": ex.get("zh", ""),
            "en": ex.get("en", ""),
            "icon": ex.get("icon", ""),
            "accent": ex.get("home_accent") or subjects.get(parent, {}).get("accent", ""),
        })
        edges.append({"source": parent, "target": key, "type": "parent"})

    # Related edges: undirected, deduped, only between existing concepts.
    seen = set()
    for key, ex in exhibits.items():
        if not ex.get("parent"):
            continue
        for target in ex.get("related", []) or []:
            if target not in concept_keys or target == key:
                continue
            pair = tuple(sorted((key, target)))
            if pair in seen:
                continue
            seen.add(pair)
            edges.append({"source": pair[0], "target": pair[1], "type": "related"})

    return {"nodes": nodes, "edges": edges}


@router.get("/api/graph")
def get_graph():
    """Return the knowledge graph structure (subjects + concepts + relations)."""
    return build_graph(settings.subjects, settings.exhibits)
