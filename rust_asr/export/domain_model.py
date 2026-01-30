"""Domain Model documentation export module.

Generates 02-domain-model/ documentation:
- core-concepts.md: Domain entities and relationships
- data-models.md: Key types with examples
- data-flow.md: Sequence diagrams
"""

from pathlib import Path
from typing import Any
import re


def analyze_domain_types(project_path: Path) -> dict[str, Any]:
    """Analyze domain types from Rust source files.
    
    Extracts:
    - Structs with their fields
    - Enums with variants
    - Type aliases
    - Trait definitions
    """
    types_info = {
        "structs": [],
        "enums": [],
        "type_aliases": [],
        "traits": [],
    }
    
    src_path = project_path / "src"
    if not src_path.exists():
        src_path = project_path
    
    struct_pattern = re.compile(r"pub\s+struct\s+(\w+)(?:<[^>]+>)?\s*\{([^}]*)\}", re.MULTILINE | re.DOTALL)
    enum_pattern = re.compile(r"pub\s+enum\s+(\w+)(?:<[^>]+>)?\s*\{([^}]*)\}", re.MULTILINE | re.DOTALL)
    trait_pattern = re.compile(r"pub\s+trait\s+(\w+)(?:<[^>]+>)?", re.MULTILINE)
    type_pattern = re.compile(r"pub\s+type\s+(\w+)\s*=\s*([^;]+);", re.MULTILINE)
    
    for rs_file in src_path.rglob("*.rs"):
        try:
            content = rs_file.read_text(errors="ignore")
            rel_path = rs_file.relative_to(project_path)
            
            for match in struct_pattern.finditer(content):
                name = match.group(1)
                fields_raw = match.group(2)
                fields = [f.strip().split(":")[0].strip() 
                         for f in fields_raw.split(",") 
                         if ":" in f and f.strip()]
                types_info["structs"].append({
                    "name": name,
                    "fields": fields[:5],
                    "file": str(rel_path),
                })
            
            for match in enum_pattern.finditer(content):
                name = match.group(1)
                variants_raw = match.group(2)
                variants = [v.strip().split("(")[0].split("{")[0].strip() 
                           for v in variants_raw.split(",") 
                           if v.strip() and not v.strip().startswith("//")]
                types_info["enums"].append({
                    "name": name,
                    "variants": variants[:5],
                    "file": str(rel_path),
                })
            
            for match in trait_pattern.finditer(content):
                name = match.group(1)
                types_info["traits"].append({
                    "name": name,
                    "file": str(rel_path),
                })
            
            for match in type_pattern.finditer(content):
                name = match.group(1)
                target = match.group(2).strip()[:50]
                types_info["type_aliases"].append({
                    "name": name,
                    "target": target,
                    "file": str(rel_path),
                })
                
        except Exception:
            continue
    
    return types_info


def generate_core_concepts(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate core-concepts.md with domain entities."""
    project_name = project_path.name
    types_info = analyze_domain_types(project_path)
    
    lines = [
        f"# Core Concepts: {project_name}",
        "",
        "## Domain Entities",
        "",
        "### Key Data Structures",
        "",
        "| Struct | Fields | File |",
        "|--------|--------|------|",
    ]
    
    for struct in types_info["structs"][:15]:
        fields_str = ", ".join(struct["fields"][:3])
        if len(struct["fields"]) > 3:
            fields_str += "..."
        lines.append(f"| `{struct['name']}` | {fields_str} | {struct['file']} |")
    
    if not types_info["structs"]:
        lines.append("| *No public structs detected* | - | - |")
    
    lines.extend([
        "",
        "### Enumerations",
        "",
        "| Enum | Variants | File |",
        "|------|----------|------|",
    ])
    
    for enum in types_info["enums"][:10]:
        variants_str = ", ".join(enum["variants"][:3])
        if len(enum["variants"]) > 3:
            variants_str += "..."
        lines.append(f"| `{enum['name']}` | {variants_str} | {enum['file']} |")
    
    if not types_info["enums"]:
        lines.append("| *No public enums detected* | - | - |")
    
    lines.extend([
        "",
        "### Core Traits",
        "",
        "| Trait | File |",
        "|-------|------|",
    ])
    
    for trait in types_info["traits"][:10]:
        lines.append(f"| `{trait['name']}` | {trait['file']} |")
    
    if not types_info["traits"]:
        lines.append("| *No public traits detected* | - |")
    
    # Entity relationship diagram
    lines.extend([
        "",
        "## Entity Relationships",
        "",
        "```mermaid",
        "erDiagram",
    ])
    
    for struct in types_info["structs"][:8]:
        name = struct["name"]
        for field in struct["fields"][:3]:
            field_clean = field.strip().replace("pub ", "")
            if field_clean:
                lines.append(f"    {name} ||--o| {field_clean} : contains")
    
    if not types_info["structs"]:
        lines.append("    DOMAIN ||--o| ENTITY : contains")
    
    lines.append("```")
    
    return "\n".join(lines)


def generate_data_models(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate data-models.md with type definitions."""
    project_name = project_path.name
    types_info = analyze_domain_types(project_path)
    
    lines = [
        f"# Data Models: {project_name}",
        "",
        "## Type Aliases",
        "",
        "| Alias | Definition | File |",
        "|-------|------------|------|",
    ]
    
    for alias in types_info["type_aliases"][:10]:
        lines.append(f"| `{alias['name']}` | `{alias['target']}` | {alias['file']} |")
    
    if not types_info["type_aliases"]:
        lines.append("| *No type aliases detected* | - | - |")
    
    lines.extend([
        "",
        "## Key Structures (Detailed)",
        "",
    ])
    
    for struct in types_info["structs"][:5]:
        lines.extend([
            f"### `{struct['name']}`",
            "",
            f"*From: {struct['file']}*",
            "",
            "**Fields:**",
        ])
        for field in struct["fields"][:5]:
            lines.append(f"- `{field}`")
        lines.append("")
    
    return "\n".join(lines)


def generate_data_flow(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate data-flow.md with sequence diagrams."""
    project_name = project_path.name
    comm_patterns = analysis.get("communication_patterns", [])
    
    lines = [
        f"# Data Flow: {project_name}",
        "",
        "## Communication Patterns",
        "",
    ]
    
    if comm_patterns:
        for pattern in comm_patterns[:3]:
            lines.extend([
                f"### {pattern['pattern']}",
                "",
                "```mermaid",
                "sequenceDiagram",
                f"    participant A as Component A",
                f"    participant B as Component B",
                f"    A->>B: {pattern['pattern']}",
                f"    B-->>A: Response",
                "```",
                "",
            ])
    else:
        lines.extend([
            "### Standard Request-Response",
            "",
            "```mermaid",
            "sequenceDiagram",
            "    participant Client",
            "    participant Core",
            "    participant Backend",
            "    Client->>Core: Request",
            "    Core->>Backend: Process",
            "    Backend-->>Core: Result",
            "    Core-->>Client: Response",
            "```",
        ])
    
    return "\n".join(lines)


def export_domain_model(
    project_path: Path,
    output_dir: Path,
    analysis: dict[str, Any],
) -> dict[str, Path]:
    """Export 02-domain-model/ documentation.
    
    Args:
        project_path: Path to Rust project
        output_dir: Output directory
        analysis: Complete analysis data
        
    Returns:
        Dict mapping file names to paths
    """
    domain_dir = Path(output_dir) / "02-domain-model"
    domain_dir.mkdir(parents=True, exist_ok=True)
    
    files = {}
    
    # core-concepts.md
    content = generate_core_concepts(project_path, analysis)
    path = domain_dir / "core-concepts.md"
    path.write_text(content)
    files["core-concepts.md"] = path
    
    # data-models.md
    content = generate_data_models(project_path, analysis)
    path = domain_dir / "data-models.md"
    path.write_text(content)
    files["data-models.md"] = path
    
    # data-flow.md
    content = generate_data_flow(project_path, analysis)
    path = domain_dir / "data-flow.md"
    path.write_text(content)
    files["data-flow.md"] = path
    
    return files
