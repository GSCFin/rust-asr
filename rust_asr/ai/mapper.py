"""Codebase-to-text mapping for LLM context."""

from pathlib import Path
from typing import Any


# Priority files for architecture understanding
PRIORITY_FILES = [
    "Cargo.toml",
    "src/lib.rs",
    "src/main.rs",
    "src/mod.rs",
    "README.md",
]


def map_codebase(project_path: Path, max_tokens: int = 100000) -> str:
    """Map codebase to LLM-friendly text format."""
    lines = []
    
    # Project header
    lines.append(f"# Codebase: {project_path.name}")
    lines.append("")
    
    # Directory structure
    lines.append("## Directory Structure")
    lines.append("```")
    lines.extend(_get_tree(project_path, max_depth=3))
    lines.append("```")
    lines.append("")
    
    # Priority files content
    lines.append("## Key Files")
    
    for pf in PRIORITY_FILES:
        file_path = project_path / pf
        if file_path.exists():
            lines.append(f"### {pf}")
            lines.append("```rust" if pf.endswith(".rs") else "```toml" if pf.endswith(".toml") else "```")
            try:
                content = file_path.read_text()
                # Truncate if too long
                if len(content) > 5000:
                    content = content[:5000] + "\n... (truncated)"
                lines.append(content)
            except Exception as e:
                lines.append(f"Error reading: {e}")
            lines.append("```")
            lines.append("")
    
    # Module listing
    lines.append("## Modules")
    src_path = project_path / "src"
    if src_path.exists():
        for rs_file in sorted(src_path.rglob("*.rs")):
            rel_path = rs_file.relative_to(project_path)
            lines.append(f"- `{rel_path}`")
    
    result = "\n".join(lines)
    
    # Rough token estimation (4 chars per token)
    if len(result) > max_tokens * 4:
        result = result[:max_tokens * 4] + "\n... (truncated for token limit)"
    
    return result


def _get_tree(path: Path, max_depth: int = 3, prefix: str = "") -> list[str]:
    """Generate directory tree."""
    lines = []
    
    if max_depth <= 0:
        return lines
    
    try:
        entries = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
    except PermissionError:
        return lines
    
    # Filter out common non-essential directories
    skip_dirs = {".git", "target", "node_modules", ".cargo", "__pycache__"}
    entries = [e for e in entries if e.name not in skip_dirs]
    
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        
        if entry.is_dir():
            lines.append(f"{prefix}{connector}{entry.name}/")
            extension = "    " if is_last else "│   "
            lines.extend(_get_tree(entry, max_depth - 1, prefix + extension))
        else:
            lines.append(f"{prefix}{connector}{entry.name}")
    
    return lines


def extract_key_types(project_path: Path) -> list[dict[str, Any]]:
    """Extract key type definitions (structs, enums, traits)."""
    types = []
    
    src_path = project_path / "src"
    if not src_path.exists():
        return types
    
    import re
    
    patterns = {
        "struct": r"pub\s+struct\s+(\w+)",
        "enum": r"pub\s+enum\s+(\w+)",
        "trait": r"pub\s+trait\s+(\w+)",
    }
    
    for rs_file in src_path.rglob("*.rs"):
        try:
            content = rs_file.read_text()
            rel_path = str(rs_file.relative_to(project_path))
            
            for type_kind, pattern in patterns.items():
                for match in re.finditer(pattern, content):
                    types.append({
                        "kind": type_kind,
                        "name": match.group(1),
                        "file": rel_path,
                    })
        except Exception:
            continue
    
    return types
