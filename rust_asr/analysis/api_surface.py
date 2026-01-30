"""Public API surface extraction for Rust projects.

Analyzes visibility modifiers to identify the public interface of a crate.
Helps determine component boundaries for C4 diagrams.
"""

import re
from pathlib import Path
from typing import Any

from .architecture import _iter_source_files


# Visibility patterns in Rust
VISIBILITY_PATTERNS = {
    "pub": r"\bpub\s+",
    "pub(crate)": r"pub\s*\(\s*crate\s*\)",
    "pub(super)": r"pub\s*\(\s*super\s*\)",
    "pub(self)": r"pub\s*\(\s*self\s*\)",
    "pub(in path)": r"pub\s*\(\s*in\s+[a-zA-Z_:]+\s*\)",
}


def analyze_api_surface(project_path: Path) -> dict[str, Any]:
    """
    Extract the public API surface of a Rust project.
    
    Returns:
        dict with public items categorized by type and visibility level
    """
    api_items: list[dict[str, Any]] = []
    
    for rs_file in _iter_source_files(project_path, include_tests=False):
        try:
            content = rs_file.read_text(errors="ignore")
            rel_path = str(rs_file.relative_to(project_path))
            
            items = _extract_pub_items(content, rel_path)
            api_items.extend(items)
        except Exception:
            continue
    
    categorized = _categorize_api(api_items)
    
    return {
        "project": project_path.name,
        "items": api_items,
        "by_type": categorized["by_type"],
        "by_visibility": categorized["by_visibility"],
        "by_module": categorized["by_module"],
        "stats": {
            "total_pub_items": len(api_items),
            "pub_structs": sum(1 for i in api_items if i["type"] == "struct"),
            "pub_enums": sum(1 for i in api_items if i["type"] == "enum"),
            "pub_traits": sum(1 for i in api_items if i["type"] == "trait"),
            "pub_functions": sum(1 for i in api_items if i["type"] == "fn"),
            "pub_modules": sum(1 for i in api_items if i["type"] == "mod"),
        }
    }


def _extract_pub_items(content: str, file_path: str) -> list[dict[str, Any]]:
    """Extract all public items from a Rust source file."""
    items = []
    
    patterns = {
        "struct": r"(pub(?:\s*\([^)]*\))?\s+)struct\s+(\w+)",
        "enum": r"(pub(?:\s*\([^)]*\))?\s+)enum\s+(\w+)",
        "trait": r"(pub(?:\s*\([^)]*\))?\s+)trait\s+(\w+)",
        "fn": r"(pub(?:\s*\([^)]*\))?\s+)(?:async\s+)?fn\s+(\w+)",
        "mod": r"(pub(?:\s*\([^)]*\))?\s+)mod\s+(\w+)",
        "type": r"(pub(?:\s*\([^)]*\))?\s+)type\s+(\w+)",
        "const": r"(pub(?:\s*\([^)]*\))?\s+)const\s+(\w+)",
        "static": r"(pub(?:\s*\([^)]*\))?\s+)static\s+(\w+)",
    }
    
    for item_type, pattern in patterns.items():
        for match in re.finditer(pattern, content):
            visibility_str = match.group(1).strip()
            name = match.group(2)
            
            if name in ["self", "Self", "crate", "super"]:
                continue
            
            visibility = _parse_visibility(visibility_str)
            
            line_number = content[:match.start()].count("\n") + 1
            
            items.append({
                "name": name,
                "type": item_type,
                "visibility": visibility,
                "visibility_raw": visibility_str,
                "file": file_path,
                "line": line_number,
            })
    
    docstrings = _extract_docstrings(content, items)
    for item in items:
        key = f"{item['type']}:{item['name']}:{item['line']}"
        if key in docstrings:
            item["doc"] = docstrings[key]
    
    return items


def _parse_visibility(vis_str: str) -> str:
    """Parse visibility string to canonical form."""
    vis_str = vis_str.strip()
    
    if re.match(r"pub\s*\(\s*crate\s*\)", vis_str):
        return "pub(crate)"
    elif re.match(r"pub\s*\(\s*super\s*\)", vis_str):
        return "pub(super)"
    elif re.match(r"pub\s*\(\s*self\s*\)", vis_str):
        return "pub(self)"
    elif re.match(r"pub\s*\(\s*in\s+", vis_str):
        return "pub(in ...)"
    elif vis_str.startswith("pub"):
        return "pub"
    return "private"


def _extract_docstrings(
    content: str, items: list[dict[str, Any]]
) -> dict[str, str]:
    """Extract doc comments for items."""
    docstrings: dict[str, str] = {}
    
    doc_pattern = r"((?:///[^\n]*\n)+|/\*\*[\s\S]*?\*/)\s*(?:pub(?:\s*\([^)]*\))?\s+)?(?:async\s+)?(?:struct|enum|trait|fn|mod|type|const|static)\s+(\w+)"
    
    for match in re.finditer(doc_pattern, content):
        doc_raw = match.group(1)
        name = match.group(2)
        
        if doc_raw.startswith("///"):
            doc = "\n".join(
                line.lstrip("/").strip()
                for line in doc_raw.split("\n")
                if line.strip().startswith("///")
            )
        else:
            doc = doc_raw.strip("/*").strip("*/").strip()
        
        if doc:
            line_num = content[:match.start()].count("\n") + 1
            for item in items:
                if item["name"] == name and abs(item["line"] - line_num) < 5:
                    key = f"{item['type']}:{item['name']}:{item['line']}"
                    docstrings[key] = doc[:200]
                    break
    
    return docstrings


def _categorize_api(items: list[dict[str, Any]]) -> dict[str, dict]:
    """Categorize API items by type, visibility, and module."""
    by_type: dict[str, list] = {}
    by_visibility: dict[str, list] = {}
    by_module: dict[str, list] = {}
    
    for item in items:
        item_type = item["type"]
        if item_type not in by_type:
            by_type[item_type] = []
        by_type[item_type].append(item["name"])
        
        vis = item["visibility"]
        if vis not in by_visibility:
            by_visibility[vis] = []
        by_visibility[vis].append(item["name"])
        
        module = Path(item["file"]).parent.as_posix()
        if module == ".":
            module = "root"
        if module not in by_module:
            by_module[module] = []
        by_module[module].append(item["name"])
    
    return {
        "by_type": by_type,
        "by_visibility": by_visibility,
        "by_module": by_module,
    }


def export_api_surface_report(api: dict[str, Any], output_path: Path) -> None:
    """Export API surface as markdown report."""
    lines = [
        f"# Public API Surface: {api['project']}",
        "",
        "## Statistics",
        "",
        f"- **Total public items:** {api['stats']['total_pub_items']}",
        f"- **Structs:** {api['stats']['pub_structs']}",
        f"- **Enums:** {api['stats']['pub_enums']}",
        f"- **Traits:** {api['stats']['pub_traits']}",
        f"- **Functions:** {api['stats']['pub_functions']}",
        f"- **Modules:** {api['stats']['pub_modules']}",
        "",
        "## By Visibility Level",
        "",
    ]
    
    for vis, names in sorted(api["by_visibility"].items()):
        lines.append(f"### `{vis}` ({len(names)} items)")
        lines.append("")
        for name in sorted(set(names))[:20]:
            lines.append(f"- `{name}`")
        if len(names) > 20:
            lines.append(f"- ... and {len(names) - 20} more")
        lines.append("")
    
    lines.extend(["## By Module", ""])
    
    for module, names in sorted(api["by_module"].items())[:15]:
        lines.append(f"### `{module}` ({len(names)} items)")
        lines.append("")
        for name in sorted(set(names))[:10]:
            lines.append(f"- `{name}`")
        if len(names) > 10:
            lines.append(f"- ... and {len(names) - 10} more")
        lines.append("")
    
    output_path.write_text("\n".join(lines))
