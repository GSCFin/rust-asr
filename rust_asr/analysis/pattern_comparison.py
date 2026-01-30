"""Pattern cross-reference analysis across multiple projects."""

from pathlib import Path
from typing import Any

from rust_asr.analysis import architecture, patterns


def compare_patterns(project_paths: list[Path]) -> dict[str, Any]:
    """Compare architectural patterns across multiple projects.
    
    Args:
        project_paths: List of paths to Rust projects
        
    Returns:
        Comparison matrix with patterns per project
    """
    results = {}
    all_patterns = set()
    all_styles = set()
    
    for project_path in project_paths:
        project_name = project_path.name
        
        # Detect architecture styles
        styles = architecture.detect_architecture_style(project_path)
        
        # Detect design patterns
        design_patterns = patterns.analyze(project_path)
        
        # Detect communication patterns
        comm = architecture.detect_communication_patterns(project_path)
        
        # Analyze workspace
        workspace = architecture.analyze_workspace(project_path)
        
        results[project_name] = {
            "styles": [s["style"] for s in styles],
            "style_details": styles,
            "design_patterns": [p["name"] for p in design_patterns],
            "pattern_details": design_patterns,
            "communication": [c["pattern"] for c in comm],
            "crate_count": workspace.get("package_count", 1),
        }
        
        all_styles.update(s["style"] for s in styles)
        all_patterns.update(p["name"] for p in design_patterns)
    
    return {
        "projects": results,
        "all_styles": sorted(all_styles),
        "all_patterns": sorted(all_patterns),
    }


def generate_comparison_matrix(comparison: dict[str, Any]) -> str:
    """Generate markdown comparison table.
    
    Args:
        comparison: Results from compare_patterns
        
    Returns:
        Markdown table string
    """
    lines = [
        "# Pattern Cross-Reference Matrix",
        "",
        "Comparison of architectural patterns across champion Rust projects.",
        "",
        "## Architecture Styles",
        "",
    ]
    
    # Architecture styles table
    projects = list(comparison["projects"].keys())
    all_styles = comparison["all_styles"]
    
    # Header
    header = "| Style | " + " | ".join(projects) + " |"
    separator = "|" + "|".join(["---"] * (len(projects) + 1)) + "|"
    lines.extend([header, separator])
    
    # Rows
    for style in all_styles:
        row = [style]
        for proj in projects:
            proj_styles = comparison["projects"][proj]["styles"]
            # Find confidence for this style
            style_details = comparison["projects"][proj]["style_details"]
            confidence = next(
                (s["confidence"] for s in style_details if s["style"] == style),
                0
            )
            if style in proj_styles:
                row.append(f"✅ {confidence:.0%}")
            else:
                row.append("❌")
        lines.append("| " + " | ".join(row) + " |")
    
    lines.extend([
        "",
        "## Design Patterns",
        "",
    ])
    
    # Design patterns table
    all_patterns = comparison["all_patterns"]
    
    header = "| Pattern | " + " | ".join(projects) + " |"
    separator = "|" + "|".join(["---"] * (len(projects) + 1)) + "|"
    lines.extend([header, separator])
    
    for pattern in all_patterns:
        row = [pattern]
        for proj in projects:
            proj_patterns = comparison["projects"][proj]["design_patterns"]
            if pattern in proj_patterns:
                row.append("✅")
            else:
                row.append("❌")
        lines.append("| " + " | ".join(row) + " |")
    
    lines.extend([
        "",
        "## Communication Patterns",
        "",
    ])
    
    # Communication patterns
    all_comm = set()
    for proj_data in comparison["projects"].values():
        all_comm.update(proj_data["communication"])
    
    header = "| Pattern | " + " | ".join(projects) + " |"
    separator = "|" + "|".join(["---"] * (len(projects) + 1)) + "|"
    lines.extend([header, separator])
    
    for pattern in sorted(all_comm):
        row = [pattern]
        for proj in projects:
            proj_comm = comparison["projects"][proj]["communication"]
            if pattern in proj_comm:
                row.append("✅")
            else:
                row.append("❌")
        lines.append("| " + " | ".join(row) + " |")
    
    lines.extend([
        "",
        "## Project Summary",
        "",
        "| Project | Crates | Primary Style | Key Patterns |",
        "|---------|--------|---------------|--------------|",
    ])
    
    for proj, data in comparison["projects"].items():
        primary_style = data["styles"][0] if data["styles"] else "N/A"
        key_patterns = ", ".join(data["design_patterns"][:3]) or "N/A"
        lines.append(f"| {proj} | {data['crate_count']} | {primary_style} | {key_patterns} |")
    
    return "\n".join(lines)


def generate_handbook_page(project_paths: list[Path], output_path: Path) -> None:
    """Generate pattern comparison handbook page.
    
    Args:
        project_paths: List of paths to Rust projects
        output_path: Path to save the markdown file
    """
    comparison = compare_patterns(project_paths)
    markdown = generate_comparison_matrix(comparison)
    output_path.write_text(markdown)
