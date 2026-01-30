"""Architecture documentation export module.

Generates structured markdown documentation for the 01-architecture section:
- system-context.md: C4 Context diagram + actors + capabilities
- high-level-design.md: Container diagram + component overview + patterns
- key-decisions.md: Inferred ADRs with evidence
- tech-stack.md: Dependencies + versions + features

Integrates data from:
- Static analysis (architecture.py, patterns.py, modules.py)
- Dynamic analysis (tracing.py, flamegraph.py)
- AI-enhanced analysis (ai_architecture.py)
"""

import json
from pathlib import Path
from typing import Any

from rust_asr.analysis import architecture, patterns as pattern_analyzer
from rust_asr.analysis.dynamic import tracing


def generate_system_context(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate system-context.md with C4 Context diagram.
    
    Includes:
    - Project overview
    - C4 Context diagram (Mermaid)
    - External dependencies with purposes
    - Key capabilities from detected patterns
    """
    project_name = project_path.name
    workspace = analysis.get("workspace", {})
    styles = analysis.get("architecture_styles", [])
    detected_patterns = analysis.get("patterns", [])
    
    # Get description
    description = "A Rust project"
    packages = workspace.get("packages", [])
    if packages:
        for pkg in packages:
            if pkg.get("name") == project_name and pkg.get("description"):
                description = pkg.get("description")
                break
    
    # Generate C4 Context diagram
    c4_context = architecture.generate_c4_context(project_path)
    
    # Collect external dependencies
    external_deps = []
    pkg_names = {p.get("name") for p in packages}
    for pkg in packages:
        for dep in pkg.get("dependencies", []):
            dep_name = dep if isinstance(dep, str) else dep.get("name", "")
            if dep_name and dep_name not in pkg_names:
                external_deps.append(dep_name)
    external_deps = list(set(external_deps))
    
    # Dependency purpose mapping
    dep_purposes = {
        "tokio": "Async runtime - provides async I/O, timers, and task scheduling",
        "serde": "Serialization framework - JSON, YAML, TOML support",
        "serde_json": "JSON serialization/deserialization",
        "clap": "CLI argument parsing with derive macros",
        "anyhow": "Error handling for applications",
        "thiserror": "Custom error types for libraries",
        "tracing": "Instrumentation and structured logging",
        "regex": "Regular expression matching",
        "rayon": "Data parallelism with parallel iterators",
        "crossbeam": "Concurrent data structures and channels",
        "async-trait": "Async methods in traits",
        "futures": "Future/Stream utilities",
        "bytes": "Efficient byte buffer operations",
        "memchr": "Optimized byte search (SIMD)",
        "walkdir": "Directory traversal",
        "ignore": "Gitignore-style filtering",
        "log": "Logging facade",
        "env_logger": "Environment-based log configuration",
        "once_cell": "Lazy static initialization",
        "parking_lot": "Faster synchronization primitives",
        "hyper": "HTTP client/server",
        "axum": "Web framework",
        "actix-web": "Actor-based web framework",
        "sqlx": "Async SQL toolkit",
        "diesel": "ORM and query builder",
    }
    
    # Build markdown
    lines = [
        f"# System Context: {project_name}",
        "",
        "## Overview",
        "",
        description,
        "",
        "## Context Diagram",
        "",
        c4_context,
        "",
        "## External Dependencies",
        "",
        "| Crate | Purpose |",
        "|-------|---------|",
    ]
    
    for dep in sorted(external_deps)[:15]:
        purpose = dep_purposes.get(dep, "Third-party library")
        lines.append(f"| `{dep}` | {purpose} |")
    
    # Key capabilities from architecture styles
    lines.extend([
        "",
        "## Key Capabilities",
        "",
    ])
    
    for style in styles[:3]:
        confidence = f"{style['confidence']:.0%}"
        lines.append(f"- **{style['style']}** ({confidence}): {style['description']}")
    
    # Add capabilities from detected patterns
    if detected_patterns:
        lines.extend(["", "### Detected Design Patterns", ""])
        for pattern in detected_patterns[:5]:
            conf = f"{pattern['confidence']:.0%}"
            lines.append(f"- **{pattern['name']}** ({conf})")
    
    return "\n".join(lines)


def generate_high_level_design(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate high-level-design.md with Container diagram and patterns.
    
    Includes:
    - Architecture style assessment
    - C4 Container diagram
    - Core components table
    - Internal dependency graph
    - Communication patterns
    - Runtime observability (tracing)
    """
    project_name = project_path.name
    workspace = analysis.get("workspace", {})
    styles = analysis.get("architecture_styles", [])
    comm_patterns = analysis.get("communication_patterns", [])
    detected_patterns = analysis.get("patterns", [])
    tracing_info = analysis.get("tracing", {})
    
    c4_container = architecture.generate_c4_container(project_path)
    
    lines = [
        f"# High-Level Design: {project_name}",
        "",
        "## Architecture Style Assessment",
        "",
        "| Style | Confidence | Description |",
        "|-------|------------|-------------|",
    ]
    
    for style in styles:
        conf = f"{style['confidence']:.0%}"
        lines.append(f"| {style['style']} | {conf} | {style['description']} |")
    
    if not styles:
        lines.append("| No specific style detected | - | - |")
    
    lines.extend([
        "",
        "## Container Diagram",
        "",
        c4_container,
        "",
        "## Core Components",
        "",
        "| Component | Type | Dependencies | Features |",
        "|-----------|------|--------------|----------|",
    ])
    
    packages = workspace.get("packages", [])
    test_patterns = ["test", "bench", "example", "stress", "fuzz"]
    
    # Filter to core packages only
    core_packages = [
        pkg for pkg in packages
        if not any(pattern in pkg.get("name", "").lower() for pattern in test_patterns)
    ]
    
    for pkg in core_packages[:15]:
        name = pkg.get("name", "unknown")
        dep_count = len(pkg.get("dependencies", []))
        feat_count = len(pkg.get("features", {}))
        
        # Detect package type
        if "macro" in name.lower():
            pkg_type = "Proc Macro"
        elif name.endswith("-sys"):
            pkg_type = "FFI Bindings"
        elif name.endswith("-derive"):
            pkg_type = "Derive Macro"
        elif name == project_name:
            pkg_type = "Core Library"
        else:
            pkg_type = "Library"
        
        lines.append(f"| `{name}` | {pkg_type} | {dep_count} | {feat_count} |")
    
    if len(packages) > len(core_packages):
        skipped = len(packages) - len(core_packages)
        lines.append(f"\n*{skipped} test/bench/example crates not shown*")
    
    # Dependency graph
    lines.extend([
        "",
        "## Internal Dependencies",
        "",
        "```mermaid",
        "graph TD",
    ])
    
    pkg_names = {pkg.get("name") for pkg in core_packages}
    edges_added = set()
    for pkg in core_packages[:15]:
        name = pkg.get("name", "")
        safe_name = name.replace("-", "_")
        for dep in pkg.get("dependencies", [])[:5]:
            dep_name = dep if isinstance(dep, str) else dep.get("name", "")
            if dep_name in pkg_names:
                safe_dep = dep_name.replace("-", "_")
                edge = (safe_name, safe_dep)
                if edge not in edges_added:
                    lines.append(f"    {safe_name} --> {safe_dep}")
                    edges_added.add(edge)
    
    if not edges_added:
        lines.append("    main[Main Crate]")
    
    lines.extend([
        "```",
        "",
        "## Communication Patterns",
        "",
        "| Pattern | Usage Count | Evidence |",
        "|---------|-------------|----------|",
    ])
    
    for pattern in comm_patterns[:5]:
        evidence = ", ".join(pattern.get("evidence", [])[:2])
        lines.append(f"| {pattern['pattern']} | {pattern['usage_count']} | `{evidence}` |")
    
    if not comm_patterns:
        lines.append("| No patterns detected | - | - |")
    
    # Design patterns section
    if detected_patterns:
        lines.extend([
            "",
            "## Design Patterns",
            "",
        ])
        for pattern in detected_patterns[:7]:
            conf = f"{pattern['confidence']:.0%}"
            lines.append(f"### {pattern['name']} ({conf})")
            lines.append("")
            lines.append("**Evidence:**")
            for ev in pattern.get("evidence", [])[:3]:
                lines.append(f"- {ev}")
            lines.append("")
    
    # Runtime observability
    if tracing_info.get("uses_tracing") or tracing_info.get("instrumented_count", 0) > 0:
        lines.extend([
            "## Runtime Observability",
            "",
            f"- **Uses `tracing`:** {'✅' if tracing_info.get('uses_tracing') else '❌'}",
            f"- **Tokio tracing:** {'✅' if tracing_info.get('uses_tokio_tracing') else '❌'}",
            f"- **Instrumented functions:** {tracing_info.get('instrumented_count', 0)}",
            "",
        ])
        
        instrumented = tracing_info.get("instrumented_functions", [])
        if instrumented:
            lines.extend([
                "### Top Instrumented Functions",
                "",
                "| Function | File |",
                "|----------|------|",
            ])
            for f in instrumented[:10]:
                lines.append(f"| `{f['function']}` | {f['file']} |")
    
    return "\n".join(lines)


def generate_key_decisions(
    project_path: Path,
    analysis: dict[str, Any],
    ai_adrs: str | None = None
) -> str:
    """Generate key-decisions.md with inferred ADRs.
    
    Sources:
    - AI-generated ADRs (if available)
    - Architecture styles (inferred)
    - Communication patterns (inferred)
    - Detected design patterns (inferred)
    """
    project_name = project_path.name
    
    # Use AI-generated ADRs if available
    if ai_adrs:
        return f"# Key Architectural Decisions: {project_name}\n\n{ai_adrs}"
    
    styles = analysis.get("architecture_styles", [])
    comm_patterns = analysis.get("communication_patterns", [])
    detected_patterns = analysis.get("patterns", [])
    
    lines = [
        f"# Key Architectural Decisions: {project_name}",
        "",
        "> These ADRs are inferred from code patterns. Manual validation recommended.",
        "",
    ]
    
    adr_num = 1
    
    # ADRs from architecture styles
    for style in styles:
        if style["confidence"] < 0.5:
            continue
        
        lines.extend([
            f"## ADR-{adr_num:03d}: Adopt {style['style']}",
            "",
            f"**Status**: Inferred (Confidence: {style['confidence']:.0%})",
            "",
            "### Context",
            "",
            f"The project requires {style['description'].lower()}.",
            "",
            "### Decision",
            "",
            f"Use {style['style']} architecture pattern.",
            "",
            "### Evidence",
            "",
        ])
        for e in style.get("evidence", [])[:5]:
            lines.append(f"- {e}")
        
        lines.extend([
            "",
            "### Consequences",
            "",
            "- Improved code organization",
            "- Clear separation of concerns",
            "",
            "---",
            "",
        ])
        adr_num += 1
    
    # ADRs from communication patterns
    for pattern in comm_patterns[:2]:
        if pattern.get("usage_count", 0) < 5:
            continue
        
        lines.extend([
            f"## ADR-{adr_num:03d}: Use {pattern['pattern']}",
            "",
            f"**Status**: Inferred (Usage Count: {pattern['usage_count']})",
            "",
            "### Context",
            "",
            "Components need safe, concurrent communication.",
            "",
            "### Decision",
            "",
            f"Adopt {pattern['pattern']} for inter-component messaging.",
            "",
            "### Evidence",
            "",
        ])
        for e in pattern.get("evidence", [])[:3]:
            lines.append(f"- `{e}`")
        
        lines.extend([
            "",
            "### Consequences",
            "",
            "- Thread-safe by design",
            "- Decoupled components",
            "",
            "---",
            "",
        ])
        adr_num += 1
    
    # ADRs from design patterns
    for pattern in detected_patterns[:3]:
        if pattern.get("confidence", 0) < 0.5:
            continue
        
        lines.extend([
            f"## ADR-{adr_num:03d}: Apply {pattern['name']} Pattern",
            "",
            f"**Status**: Inferred (Confidence: {pattern['confidence']:.0%})",
            "",
            "### Context",
            "",
            f"The codebase applies the {pattern['name']} pattern.",
            "",
            "### Evidence",
            "",
        ])
        for e in pattern.get("evidence", [])[:3]:
            lines.append(f"- {e}")
        
        lines.extend([
            "",
            "---",
            "",
        ])
        adr_num += 1
    
    if adr_num == 1:
        lines.append("*No high-confidence ADRs could be inferred. Consider AI-enhanced analysis.*")
    
    return "\n".join(lines)


def generate_tech_stack(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate tech-stack.md with complete dependency inventory.
    
    Includes:
    - Rust version and edition
    - Core dependencies with versions and purposes
    - Feature flags
    - Workspace structure (if applicable)
    - Build/dev tools
    """
    project_name = project_path.name
    workspace = analysis.get("workspace", {})
    packages = workspace.get("packages", [])
    
    # Get Rust version
    rust_version = "Unknown"
    rust_toolchain = project_path / "rust-toolchain.toml"
    if rust_toolchain.exists():
        try:
            content = rust_toolchain.read_text()
            for line in content.split("\n"):
                if "channel" in line and "=" in line:
                    rust_version = line.split("=")[1].strip().strip('"')
                    break
        except Exception:
            pass
    
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
    
    lines = [
        f"# Tech Stack: {project_name}",
        "",
        "## Rust Configuration",
        "",
        f"- **Edition**: {edition}",
        f"- **Toolchain**: {rust_version}",
        "",
        "## Core Dependencies",
        "",
        "| Crate | Purpose |",
        "|-------|---------|",
    ]
    
    # Dependency purpose mapping
    purposes = {
        "tokio": "Async runtime with work-stealing scheduler",
        "serde": "Serialization/deserialization framework",
        "serde_json": "JSON support for serde",
        "clap": "Command-line argument parsing",
        "anyhow": "Application error handling",
        "thiserror": "Library error types",
        "tracing": "Instrumentation and logging",
        "log": "Logging facade",
        "regex": "Regular expressions",
        "rayon": "Data parallelism",
        "crossbeam": "Concurrent primitives",
        "walkdir": "Directory traversal",
        "ignore": "Gitignore filtering",
        "memchr": "SIMD-optimized byte search",
        "bytes": "Byte buffer utilities",
        "parking_lot": "Fast synchronization",
        "once_cell": "Lazy initialization",
        "hyper": "HTTP implementation",
        "axum": "Ergonomic web framework",
        "sqlx": "Async SQL toolkit",
    }
    
    # Collect all unique dependencies
    all_deps: set[str] = set()
    for pkg in packages:
        for dep in pkg.get("dependencies", []):
            dep_name = dep if isinstance(dep, str) else dep.get("name", "")
            if dep_name:
                all_deps.add(dep_name)
    
    # Filter to notable/known dependencies first
    notable_deps = [d for d in sorted(all_deps) if d in purposes]
    other_deps = [d for d in sorted(all_deps) if d not in purposes]
    
    for dep in notable_deps[:15]:
        lines.append(f"| `{dep}` | {purposes[dep]} |")
    
    for dep in other_deps[:5]:
        lines.append(f"| `{dep}` | Third-party dependency |")
    
    # Feature flags
    lines.extend([
        "",
        "## Feature Flags",
        "",
        "| Feature | Crate | Dependencies |",
        "|---------|-------|--------------|",
    ])
    
    for pkg in packages[:8]:
        features = pkg.get("features", {})
        if isinstance(features, dict):
            for feat_name, feat_deps in list(features.items())[:3]:
                deps_str = ", ".join(feat_deps[:3]) if feat_deps else "-"
                lines.append(f"| `{feat_name}` | `{pkg.get('name')}` | {deps_str} |")
    
    # Workspace structure
    if workspace.get("is_workspace"):
        lines.extend([
            "",
            f"## Workspace Structure ({len(packages)} crates)",
            "",
            "| Crate | Dependencies | Description |",
            "|-------|--------------|-------------|",
        ])
        
        for pkg in packages[:20]:
            name = pkg.get("name", "")
            dep_count = len(pkg.get("dependencies", []))
            desc = (pkg.get("description") or "-")[:40]
            lines.append(f"| `{name}` | {dep_count} | {desc} |")
    
    return "\n".join(lines)


def export_architecture_docs(
    project_path: Path,
    output_dir: Path,
    ai_adrs: str | None = None,
    include_patterns: bool = True,
    include_tracing: bool = True,
) -> dict[str, Path]:
    """Export complete 01-architecture documentation.
    
    Args:
        project_path: Path to Rust project
        output_dir: Output directory for docs
        ai_adrs: Optional AI-generated ADRs content
        include_patterns: Include pattern detection
        include_tracing: Include tracing analysis
        
    Returns:
        Dict mapping file names to paths
    """
    project_path = Path(project_path)
    arch_dir = Path(output_dir) / "01-architecture"
    arch_dir.mkdir(parents=True, exist_ok=True)
    
    # Run comprehensive analysis
    analysis = architecture.analyze(project_path, include_dynamic=include_tracing)
    
    # Add pattern detection
    if include_patterns:
        analysis["patterns"] = pattern_analyzer.analyze(project_path)
    
    # Generate files
    files = {}
    
    # system-context.md
    system_context = generate_system_context(project_path, analysis)
    system_context_path = arch_dir / "system-context.md"
    system_context_path.write_text(system_context)
    files["system-context.md"] = system_context_path
    
    # high-level-design.md
    high_level = generate_high_level_design(project_path, analysis)
    high_level_path = arch_dir / "high-level-design.md"
    high_level_path.write_text(high_level)
    files["high-level-design.md"] = high_level_path
    
    # key-decisions.md
    key_decisions = generate_key_decisions(project_path, analysis, ai_adrs)
    key_decisions_path = arch_dir / "key-decisions.md"
    key_decisions_path.write_text(key_decisions)
    files["key-decisions.md"] = key_decisions_path
    
    # tech-stack.md
    tech_stack = generate_tech_stack(project_path, analysis)
    tech_stack_path = arch_dir / "tech-stack.md"
    tech_stack_path.write_text(tech_stack)
    files["tech-stack.md"] = tech_stack_path
    
    return files
