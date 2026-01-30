"""Dependency graph analysis using cargo-depgraph."""

import subprocess
import re
from pathlib import Path
from typing import Any

import networkx as nx


def analyze(project_path: Path) -> dict[str, Any]:
    """Analyze project dependencies and build graph."""
    # Try cargo-depgraph first
    try:
        result = subprocess.run(
            ["cargo", "depgraph", "--all-deps"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            return _parse_dot(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Fallback to cargo-tree
    try:
        result = subprocess.run(
            ["cargo", "tree", "--prefix", "none"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            return _parse_tree(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Final fallback: parse Cargo.toml
    return _parse_cargo_toml(project_path)


def _parse_dot(dot_output: str) -> dict[str, Any]:
    """Parse DOT format from cargo-depgraph."""
    G = nx.DiGraph()
    
    # Parse nodes
    node_pattern = r'"([^"]+)"'
    edge_pattern = r'"([^"]+)"\s*->\s*"([^"]+)"'
    
    for match in re.finditer(edge_pattern, dot_output):
        source, target = match.groups()
        G.add_edge(source, target)
    
    # Calculate in-degree and out-degree
    nodes = []
    for node in G.nodes():
        nodes.append({
            "name": node,
            "in_degree": G.in_degree(node),
            "out_degree": G.out_degree(node),
        })
    
    edges = [{"from": u, "to": v} for u, v in G.edges()]
    
    return {"nodes": nodes, "edges": edges}


def _parse_tree(tree_output: str) -> dict[str, Any]:
    """Parse output from cargo-tree."""
    nodes = set()
    edges = []
    
    lines = tree_output.strip().split("\n")
    for line in lines:
        # Extract crate name
        match = re.match(r"([a-zA-Z0-9_-]+)", line.strip())
        if match:
            nodes.add(match.group(1))
    
    return {
        "nodes": [{"name": n, "in_degree": 0, "out_degree": 0} for n in nodes],
        "edges": edges,
    }


def _parse_cargo_toml(project_path: Path) -> dict[str, Any]:
    """Parse Cargo.toml for dependencies."""
    import toml
    
    cargo_toml = project_path / "Cargo.toml"
    if not cargo_toml.exists():
        return {"nodes": [], "edges": []}
    
    data = toml.loads(cargo_toml.read_text())
    
    # Get package name
    pkg_name = data.get("package", {}).get("name", project_path.name)
    
    # Get dependencies
    deps = list(data.get("dependencies", {}).keys())
    dev_deps = list(data.get("dev-dependencies", {}).keys())
    
    nodes = [{"name": pkg_name, "in_degree": 0, "out_degree": len(deps)}]
    for dep in deps + dev_deps:
        nodes.append({"name": dep, "in_degree": 1, "out_degree": 0})
    
    edges = [{"from": pkg_name, "to": dep} for dep in deps]
    
    return {"nodes": nodes, "edges": edges}


def to_mermaid(graph: dict[str, Any]) -> str:
    """Convert graph to Mermaid diagram."""
    lines = ["graph TD"]
    
    for edge in graph.get("edges", []):
        source = edge["from"].replace("-", "_")
        target = edge["to"].replace("-", "_")
        lines.append(f"    {source} --> {target}")
    
    return "\n".join(lines)


def to_dot(graph: dict[str, Any]) -> str:
    """Convert graph to DOT format."""
    lines = ["digraph dependencies {"]
    
    for edge in graph.get("edges", []):
        lines.append(f'    "{edge["from"]}" -> "{edge["to"]}"')
    
    lines.append("}")
    return "\n".join(lines)


def export_mermaid(graph: dict[str, Any], output: Path) -> None:
    """Export graph as Mermaid markdown."""
    content = f"""# Dependency Graph

```mermaid
{to_mermaid(graph)}
```

## Statistics

| Metric | Value |
|--------|-------|
| Total Crates | {len(graph.get('nodes', []))} |
| Dependencies | {len(graph.get('edges', []))} |

## Core Components (High In-Degree)

| Crate | In-Degree |
|-------|-----------|
"""
    for node in sorted(graph.get("nodes", []), key=lambda x: x.get("in_degree", 0), reverse=True)[:10]:
        content += f"| {node['name']} | {node.get('in_degree', 0)} |\n"
    
    output.write_text(content)
