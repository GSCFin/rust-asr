"""Semantic Index - Navigation hints for LLM."""

from pathlib import Path
from typing import Any
import json


def build_semantic_index(
    project_path: Path,
    graph: dict[str, Any],
) -> dict[str, Any]:
    """
    Build a semantic index to help LLM navigate the codebase efficiently.
    
    Features:
    - File-to-concepts mapping
    - Concept-to-files reverse mapping
    - Hot spots identification (high-degree nodes)
    - Entry points detection (main, lib, public APIs)
    """
    file_to_concepts: dict[str, list[str]] = {}
    concept_to_files: dict[str, list[str]] = {}
    
    for node in graph.get("nodes", []):
        module = node.get("module", "")
        name = node.get("id", "")
        
        if module not in file_to_concepts:
            file_to_concepts[module] = []
        file_to_concepts[module].append(name)
        
        if name not in concept_to_files:
            concept_to_files[name] = []
        if module not in concept_to_files[name]:
            concept_to_files[name].append(module)
    
    node_degree: dict[str, int] = {}
    for edge in graph.get("edges", []):
        from_node = edge.get("from", "")
        to_node = edge.get("to", "")
        node_degree[from_node] = node_degree.get(from_node, 0) + 1
        node_degree[to_node] = node_degree.get(to_node, 0) + 1
    
    hot_spots = sorted(node_degree.items(), key=lambda x: -x[1])[:20]
    
    entry_points = _detect_entry_points(project_path, graph)
    
    public_apis = [
        node for node in graph.get("nodes", [])
        if node.get("visibility") == "pub" and node.get("type") in ["fn", "struct", "trait"]
    ]
    
    return {
        "project": graph.get("project", project_path.name),
        "file_to_concepts": file_to_concepts,
        "concept_to_files": concept_to_files,
        "hot_spots": [{"name": name, "degree": degree} for name, degree in hot_spots],
        "entry_points": entry_points,
        "public_apis": [{"name": api["name"], "type": api["type"], "module": api["module"]} 
                       for api in public_apis[:50]],
        "stats": {
            "total_files": len(file_to_concepts),
            "total_concepts": len(concept_to_files),
            "total_public_apis": len(public_apis),
        }
    }


def _detect_entry_points(project_path: Path, graph: dict[str, Any]) -> list[dict[str, str]]:
    """Detect main entry points in the codebase."""
    entry_points = []
    
    main_files = [
        ("src/main.rs", "Binary entry point"),
        ("src/lib.rs", "Library entry point"),
        ("lib.rs", "Library entry point"),
        ("main.rs", "Binary entry point"),
    ]
    
    for file_name, description in main_files:
        file_path = project_path / file_name
        if file_path.exists():
            entry_points.append({
                "file": file_name,
                "type": "main" if "main" in file_name else "lib",
                "description": description,
            })
    
    for node in graph.get("nodes", []):
        if node.get("name") == "main" and node.get("type") == "fn":
            entry_points.append({
                "file": node.get("module", ""),
                "type": "main_function",
                "description": "main() function",
            })
            break
    
    return entry_points


def export_semantic_index(index: dict[str, Any], output_path: Path) -> None:
    """Export semantic index to JSON file."""
    output_path.write_text(json.dumps(index, indent=2))


def export_semantic_index_markdown(index: dict[str, Any], output_path: Path) -> None:
    """Export a human-readable summary of the semantic index."""
    lines = [
        f"# Semantic Index: {index['project']}",
        "",
        "## Quick Navigation Guide",
        "",
        "### Entry Points",
        "Start here to understand the codebase:",
    ]
    
    for ep in index.get("entry_points", []):
        lines.append(f"- **{ep['file']}** - {ep['description']}")
    
    lines.extend([
        "",
        "### Hot Spots (Most Connected)",
        "Key components with many relationships:",
    ])
    
    for hs in index.get("hot_spots", [])[:10]:
        lines.append(f"- `{hs['name']}` ({hs['degree']} connections)")
    
    lines.extend([
        "",
        "### Public APIs",
        "Exported interfaces:",
    ])
    
    for api in index.get("public_apis", [])[:15]:
        lines.append(f"- `{api['name']}` ({api['type']}) in `{api['module']}`")
    
    if len(index.get("public_apis", [])) > 15:
        lines.append(f"- ... and {len(index['public_apis']) - 15} more")
    
    lines.extend([
        "",
        "### File Overview",
        f"- Total files with entities: {index['stats']['total_files']}",
        f"- Total named concepts: {index['stats']['total_concepts']}",
        f"- Total public APIs: {index['stats']['total_public_apis']}",
    ])
    
    output_path.write_text("\n".join(lines))
