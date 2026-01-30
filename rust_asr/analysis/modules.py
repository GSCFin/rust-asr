"""Module structure analysis using cargo-modules."""

import subprocess
import re
from pathlib import Path
from typing import Any


def analyze(project_path: Path, public_only: bool = False) -> dict[str, Any]:
    """Analyze module structure of a Rust project."""
    # Try cargo-modules first
    try:
        cmd = ["cargo", "modules", "structure"]
        if public_only:
            cmd.append("--pub")
        
        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            return _parse_modules_output(result.stdout, project_path.name)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Fallback: parse file structure
    return _parse_file_structure(project_path)


def _parse_modules_output(output: str, root_name: str) -> dict[str, Any]:
    """Parse cargo-modules structure output."""
    root: dict[str, Any] = {"name": root_name, "visibility": "pub", "children": []}
    current_stack = [root]
    
    for line in output.strip().split("\n"):
        if not line.strip():
            continue
        
        # Detect indentation level
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        level = indent // 4 + 1
        
        # Parse visibility and name
        visibility = "private"
        name = stripped
        
        if stripped.startswith("pub "):
            visibility = "pub"
            name = stripped[4:]
        elif stripped.startswith("pub(crate) "):
            visibility = "pub(crate)"
            name = stripped[11:]
        
        # Clean name
        name = name.strip().split()[0] if name else "unknown"
        
        node = {"name": name, "visibility": visibility, "children": []}
        
        # Adjust stack
        while len(current_stack) > level:
            current_stack.pop()
        
        if current_stack:
            current_stack[-1]["children"].append(node)
        current_stack.append(node)
    
    return root


def _parse_file_structure(project_path: Path) -> dict[str, Any]:
    """Parse module structure from file layout."""
    src_path = project_path / "src"
    if not src_path.exists():
        return {"name": project_path.name, "visibility": "pub", "children": []}
    
    root = {"name": project_path.name, "visibility": "pub", "children": []}
    
    # Find all .rs files
    for rs_file in src_path.rglob("*.rs"):
        rel_path = rs_file.relative_to(src_path)
        parts = list(rel_path.parts)
        
        # Skip lib.rs/main.rs at root level
        if len(parts) == 1 and parts[0] in ("lib.rs", "main.rs"):
            continue
        
        # Navigate/create path
        current = root
        for i, part in enumerate(parts[:-1]):
            # Find or create directory node
            existing = next((c for c in current["children"] if c["name"] == part), None)
            if existing:
                current = existing
            else:
                node = {"name": part, "visibility": _detect_visibility(rs_file), "children": []}
                current["children"].append(node)
                current = node
        
        # Add file node
        file_name = parts[-1].replace(".rs", "")
        if file_name not in ("mod", "lib", "main"):
            visibility = _detect_visibility(rs_file)
            current["children"].append({
                "name": file_name,
                "visibility": visibility,
                "children": [],
            })
    
    return root


def _detect_visibility(rs_file: Path) -> str:
    """Detect visibility of a module from its file content."""
    try:
        content = rs_file.read_text()
        # Simple heuristic: count pub items
        pub_count = len(re.findall(r"\bpub\s+(?:fn|struct|enum|trait|mod|type|const|static)", content))
        if pub_count > 0:
            return "pub"
        return "private"
    except Exception:
        return "unknown"


def export_tree(tree: dict[str, Any], output: Path) -> None:
    """Export module tree as markdown."""
    lines = ["# Module Structure", "", "```"]
    _tree_to_lines(tree, lines, 0)
    lines.append("```")
    
    output.write_text("\n".join(lines))


def _tree_to_lines(node: dict[str, Any], lines: list[str], depth: int) -> None:
    """Convert tree node to lines."""
    indent = "  " * depth
    visibility = node.get("visibility", "")
    vis_marker = f" ({visibility})" if visibility else ""
    lines.append(f"{indent}└── {node['name']}{vis_marker}")
    
    for child in node.get("children", []):
        _tree_to_lines(child, lines, depth + 1)
