"""Executive Summary documentation export module.

Generates 00-executive-summary.md:
- Project overview (1-2 sentences)
- Tech stack summary
- Key decisions bullet points
- Quick navigation links
"""

from pathlib import Path
from typing import Any


def generate_executive_summary(
    project_path: Path,
    analysis: dict[str, Any],
    sections_generated: list[str] | None = None
) -> str:
    """Generate 00-executive-summary.md with TL;DR overview.
    
    Args:
        project_path: Path to Rust project
        analysis: Complete analysis data
        sections_generated: List of generated section names for navigation
    """
    project_name = project_path.name
    workspace = analysis.get("workspace", {})
    styles = analysis.get("architecture_styles", [])
    patterns = analysis.get("patterns", [])
    packages = workspace.get("packages", [])
    
    # Get project description
    description = "A Rust project"
    for pkg in packages:
        if pkg.get("name") == project_name and pkg.get("description"):
            description = pkg.get("description")
            break
    
    # Get edition
    edition = "2021"
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text()
            for line in content.split("\n"):
                if line.strip().startswith("edition"):
                    edition = line.split("=")[1].strip().strip('"')
                    break
        except Exception:
            pass
    
    # Build tech stack summary
    notable_deps = []
    dep_categories = {
        "tokio": "Async",
        "serde": "Serialization",
        "clap": "CLI",
        "axum": "Web",
        "sqlx": "Database",
        "tracing": "Observability",
        "rayon": "Parallelism",
        "anyhow": "Error Handling",
    }
    
    all_deps = set()
    for pkg in packages:
        for dep in pkg.get("dependencies", []):
            dep_name = dep if isinstance(dep, str) else dep.get("name", "")
            if dep_name in dep_categories:
                notable_deps.append(f"{dep_categories[dep_name]} (`{dep_name}`)")
                all_deps.add(dep_name)
    
    tech_stack_summary = ", ".join(notable_deps[:5]) if notable_deps else "Standard library focused"
    
    lines = [
        f"# {project_name}",
        "",
        "## At a Glance",
        "",
        f"> {description}",
        "",
        "| Attribute | Value |",
        "|-----------|-------|",
        f"| **Edition** | Rust {edition} |",
        f"| **Crates** | {len(packages)} |",
        f"| **Tech Focus** | {tech_stack_summary} |",
        "",
    ]
    
    # Architecture style
    if styles:
        top_style = styles[0]
        lines.extend([
            "## Architecture",
            "",
            f"**Primary Style:** {top_style['style']} ({top_style['confidence']:.0%} confidence)",
            "",
            f"{top_style['description']}",
            "",
        ])
    
    # Key decisions (top 3)
    lines.extend([
        "## Key Decisions",
        "",
    ])
    
    decision_count = 0
    for style in styles[:2]:
        if style["confidence"] >= 0.5:
            lines.append(f"- ✅ **{style['style']}** architecture pattern")
            decision_count += 1
    
    for pattern in patterns[:2]:
        if pattern.get("confidence", 0) >= 0.5:
            lines.append(f"- ✅ **{pattern['name']}** design pattern")
            decision_count += 1
    
    if decision_count == 0:
        lines.append("- See [key-decisions.md](01-architecture/key-decisions.md) for inferred ADRs")
    
    lines.append("")
    
    # Navigation
    lines.extend([
        "## Documentation",
        "",
        "| Section | Description |",
        "|---------|-------------|",
        "| [01-architecture](01-architecture/) | System context, design, decisions |",
        "| [02-domain-model](02-domain-model/) | Core concepts and data models |",
        "| [03-api-interfaces](03-api-interfaces/) | Public APIs and contracts |",
        "| [04-critical-paths](04-critical-paths/) | Main flows and hotspots |",
        "| [05-development-guide](05-development-guide/) | Getting started and conventions |",
    ])
    
    return "\n".join(lines)


def export_executive_summary(
    project_path: Path,
    output_dir: Path,
    analysis: dict[str, Any],
) -> Path:
    """Export 00-executive-summary.md.
    
    Args:
        project_path: Path to Rust project
        output_dir: Output directory
        analysis: Complete analysis data
        
    Returns:
        Path to generated file
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    content = generate_executive_summary(project_path, analysis)
    output_path = output_dir / "00-executive-summary.md"
    output_path.write_text(content)
    
    return output_path
