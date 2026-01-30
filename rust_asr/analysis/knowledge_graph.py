"""Knowledge Graph extraction from Rust codebase."""

import json
import re
from pathlib import Path
from typing import Any


def build_knowledge_graph(project_path: Path) -> dict[str, Any]:
    """
    Build a knowledge graph from the Rust codebase.
    
    Extracts entities (structs, enums, traits, functions) and their relationships
    (uses, implements, depends_on) to create a navigable graph for LLM analysis.
    
    Returns:
        dict with nodes, edges, and clusters
    """
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    
    entity_map: dict[str, dict[str, Any]] = {}
    
    src_paths = [project_path / "src"]
    if not src_paths[0].exists():
        src_paths = [project_path]
    
    for src_path in src_paths:
        for rs_file in src_path.rglob("*.rs"):
            if "target" in rs_file.parts:
                continue
            
            try:
                content = rs_file.read_text(errors="ignore")
                rel_path = str(rs_file.relative_to(project_path))
                
                file_entities = _extract_entities(content, rel_path)
                for entity in file_entities:
                    entity_id = f"{entity['name']}"
                    if entity_id not in entity_map:
                        entity_map[entity_id] = entity
                        nodes.append(entity)
                
                file_edges = _extract_relationships(content, rel_path, entity_map)
                edges.extend(file_edges)
                
            except Exception:
                continue
    
    clusters = _identify_clusters(nodes, edges)
    
    return {
        "project": project_path.name,
        "nodes": nodes,
        "edges": edges,
        "clusters": clusters,
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "total_clusters": len(clusters),
        }
    }


def _extract_entities(content: str, file_path: str) -> list[dict[str, Any]]:
    """Extract struct, enum, trait, and function definitions."""
    entities = []
    
    patterns = {
        "struct": r"(?:pub(?:\([^)]+\))?\s+)?struct\s+(\w+)",
        "enum": r"(?:pub(?:\([^)]+\))?\s+)?enum\s+(\w+)",
        "trait": r"(?:pub(?:\([^)]+\))?\s+)?trait\s+(\w+)",
        "impl": r"impl(?:<[^>]+>)?\s+(\w+)",
        "fn": r"(?:pub(?:\([^)]+\))?\s+)?(?:async\s+)?fn\s+(\w+)",
    }
    
    for entity_type, pattern in patterns.items():
        for match in re.finditer(pattern, content):
            name = match.group(1)
            
            if name in ["self", "Self", "new", "default", "from", "into"]:
                continue
            
            visibility = "pub" if "pub " in content[max(0, match.start()-10):match.start()+10] else "private"
            
            entities.append({
                "id": name,
                "name": name,
                "type": entity_type,
                "module": file_path,
                "visibility": visibility,
            })
    
    return entities


def _extract_relationships(
    content: str,
    file_path: str,
    entity_map: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Extract relationships between entities with semantic edge types."""
    edges = []
    
    # Trait implementations: impl Trait for Type
    impl_pattern = r"impl(?:<[^>]+>)?\s+(\w+)(?:<[^>]+>)?\s+for\s+(\w+)"
    for match in re.finditer(impl_pattern, content):
        trait_name = match.group(1)
        struct_name = match.group(2)
        edges.append({
            "from": struct_name,
            "to": trait_name,
            "relationship": "implements",
            "source": file_path,
        })
    
    # Derive attributes: #[derive(Trait1, Trait2)]
    derive_pattern = r"#\[derive\(([^)]+)\)\]\s*(?:pub(?:\([^)]*\))?\s+)?(?:struct|enum)\s+(\w+)"
    for match in re.finditer(derive_pattern, content):
        derives = [t.strip() for t in match.group(1).split(",")]
        type_name = match.group(2)
        for derive_trait in derives:
            edges.append({
                "from": type_name,
                "to": derive_trait,
                "relationship": "derives",
                "source": file_path,
            })
    
    # Module containment: mod name { ... } or pub mod name;
    module_stack = [Path(file_path).stem]
    mod_pattern = r"(?:pub(?:\([^)]*\))?\s+)?mod\s+(\w+)"
    for match in re.finditer(mod_pattern, content):
        mod_name = match.group(1)
        parent = module_stack[-1] if module_stack else "root"
        edges.append({
            "from": parent,
            "to": mod_name,
            "relationship": "contains",
            "source": file_path,
        })
    
    # Use/import relationships
    use_pattern = r"use\s+(?:crate::)?([a-zA-Z_][a-zA-Z0-9_:]*)"
    for match in re.finditer(use_pattern, content):
        import_path = match.group(1)
        parts = import_path.split("::")
        if parts:
            imported = parts[-1]
            if imported in entity_map:
                module_name = Path(file_path).stem
                edges.append({
                    "from": module_name,
                    "to": imported,
                    "relationship": "uses",
                    "source": file_path,
                })
    
    # Field type references
    field_pattern = r"(\w+)\s*:\s*(?:&)?(?:mut\s+)?(?:Option<|Vec<|Box<|Arc<|Rc<)?(\w+)"
    for match in re.finditer(field_pattern, content):
        field_type = match.group(2)
        primitives = {"str", "String", "usize", "isize", "i8", "i16", "i32", "i64", 
                      "u8", "u16", "u32", "u64", "f32", "f64", "bool", "char", "Self"}
        if field_type in entity_map and field_type not in primitives:
            edges.append({
                "from": "field_usage",
                "to": field_type,
                "relationship": "references",
                "source": file_path,
            })
    
    return edges


def _identify_clusters(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Identify logical clusters/layers based on module paths and relationships."""
    clusters: dict[str, list[str]] = {}
    
    for node in nodes:
        module = node.get("module", "")
        
        if "domain" in module or "entity" in module or "model" in module:
            layer = "Domain Layer"
        elif "service" in module or "application" in module or "handler" in module:
            layer = "Application Layer"
        elif "repo" in module or "db" in module or "storage" in module:
            layer = "Infrastructure Layer"
        elif "api" in module or "http" in module or "web" in module:
            layer = "Interface Layer"
        elif "util" in module or "common" in module or "helper" in module:
            layer = "Utilities"
        else:
            parts = module.split("/")
            if len(parts) > 1:
                layer = f"Module: {parts[-2] if parts[-1].endswith('.rs') else parts[-1]}"
            else:
                layer = "Core"
        
        if layer not in clusters:
            clusters[layer] = []
        clusters[layer].append(node["id"])
    
    return [
        {"name": name, "nodes": sorted(set(node_ids))}
        for name, node_ids in sorted(clusters.items())
    ]


def export_knowledge_graph(graph: dict[str, Any], output_path: Path) -> None:
    """Export knowledge graph to JSON file."""
    output_path.write_text(json.dumps(graph, indent=2))


def export_knowledge_graph_summary(graph: dict[str, Any], output_path: Path) -> None:
    """Export a human-readable summary of the knowledge graph."""
    lines = [
        f"# Knowledge Graph: {graph['project']}",
        "",
        "## Statistics",
        f"- **Nodes:** {graph['stats']['total_nodes']}",
        f"- **Edges:** {graph['stats']['total_edges']}",
        f"- **Clusters:** {graph['stats']['total_clusters']}",
        "",
        "## Entity Types",
    ]
    
    type_counts: dict[str, int] = {}
    for node in graph["nodes"]:
        t = node["type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    
    for entity_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {entity_type}: {count}")
    
    lines.extend(["", "## Clusters (Layers)"])
    for cluster in graph["clusters"]:
        lines.append(f"### {cluster['name']}")
        for node_id in cluster["nodes"][:10]:
            lines.append(f"- {node_id}")
        if len(cluster["nodes"]) > 10:
            lines.append(f"- ... and {len(cluster['nodes']) - 10} more")
        lines.append("")
    
    lines.extend(["", "## Key Relationships"])
    rel_counts: dict[str, int] = {}
    for edge in graph["edges"]:
        rel = edge["relationship"]
        rel_counts[rel] = rel_counts.get(rel, 0) + 1
    
    for rel, count in sorted(rel_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {rel}: {count} connections")
    
    output_path.write_text("\n".join(lines))
