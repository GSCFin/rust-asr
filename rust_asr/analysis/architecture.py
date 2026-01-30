"""System architecture analysis for Rust projects.

Extracts high-level architectural patterns including:
- Workspace structure analysis
- C4 diagram generation (Context, Container, Component)
- Architectural style detection
- Communication patterns between components
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Iterator


# Patterns to exclude from source code analysis (test/bench/example files)
EXCLUDE_PATH_PATTERNS = [
    "/tests/", "/test/", "/benches/", "/bench/", "/examples/", "/example/",
    "_test.rs", "_tests.rs", "_bench.rs", "/fuzz/", "/stress/",
]


def _is_test_file(file_path: Path, project_path: Path) -> bool:
    """Check if a file is a test/bench/example file that should be excluded."""
    rel_path = str(file_path.relative_to(project_path))
    for pattern in EXCLUDE_PATH_PATTERNS:
        if pattern in rel_path or rel_path.endswith(pattern.strip("/")):
            return True
    return False


def _iter_source_files(project_path: Path, include_tests: bool = False) -> Iterator[Path]:
    """Iterate over Rust source files, optionally filtering out test code."""
    src_path = project_path / "src"
    if not src_path.exists():
        src_path = project_path
    
    for rs_file in src_path.rglob("*.rs"):
        if include_tests or not _is_test_file(rs_file, project_path):
            yield rs_file


# Architecture style signatures - enhanced with Rust-specific patterns from research
ARCHITECTURE_STYLES = {
    "Modular Monolith": {
        "indicators": ["single_crate", "many_modules"],
        "description": "Single crate with well-organized internal modules by domain",
    },
    "Multi-Crate Workspace": {
        "indicators": ["workspace", "multiple_crates"],
        "description": "Multiple crates in a workspace, each with specific responsibility",
    },
    "Plugin Architecture": {
        "indicators": ["plugin", "Plugin", "add_plugin", "PluginGroup"],
        "description": "Core system with extensible plugin-based functionality",
    },
    "Hexagonal/Ports-Adapters": {
        "indicators": ["port", "adapter", "domain", "infrastructure", "Storage", "Backend"],
        "description": "Domain logic separated from infrastructure through traits (pluggable storage)",
    },
    "Event-Driven": {
        "indicators": ["Event", "EventReader", "EventWriter", "on_event", "emit"],
        "description": "Components communicate through events and messages",
    },
    "Actor Model": {
        "indicators": ["actix", "xactor", "ractor", "Addr<", "Handler<"],
        "description": "Concurrent computation using actors with message mailboxes",
    },
    "Reactor/Proactor": {
        "indicators": ["Future", "Poll::", "Waker", "async fn", ".await", "executor"],
        "description": "Async I/O with event loop (Tokio, async-std style)",
    },
    "Work-Stealing Scheduler": {
        "indicators": ["work_steal", "multi_thread", "Runtime::new", "tokio::runtime"],
        "description": "Load-balanced task scheduling across worker threads",
    },
    "ECS (Entity-Component-System)": {
        "indicators": ["bevy_ecs", "specs", "legion", "hecs", "World", "Query<"],
        "description": "Data-oriented design with entities, components, and systems",
    },
}


# Communication pattern signatures
COMMUNICATION_PATTERNS = {
    "Channel-based (tokio)": ["tokio::sync::mpsc", "tokio::sync::oneshot", "tokio::sync::broadcast"],
    "Channel-based (crossbeam)": ["crossbeam-channel", "crossbeam::channel"],
    "Shared State (Mutex)": ["Arc<Mutex", "Mutex<", "std::sync::Mutex"],
    "Shared State (RwLock)": ["Arc<RwLock", "RwLock<", "std::sync::RwLock"],
    "Async Channels": ["async_channel", "flume"],
    "Message Passing": ["actix", "xactor", "ractor"],
}


def analyze_workspace(project_path: Path) -> dict[str, Any]:
    """Analyze workspace structure using cargo metadata."""
    try:
        result = subprocess.run(
            ["cargo", "metadata", "--format-version", "1", "--no-deps"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            return {"error": result.stderr, "is_workspace": False}
        
        metadata = json.loads(result.stdout)
        packages = metadata.get("packages", [])
        workspace_root = metadata.get("workspace_root", str(project_path))
        workspace_members = metadata.get("workspace_members", [])
        
        return {
            "is_workspace": len(packages) > 1,
            "workspace_root": workspace_root,
            "package_count": len(packages),
            "packages": [
                {
                    "name": pkg["name"],
                    "version": pkg["version"],
                    "description": pkg.get("description", ""),
                    "dependencies": [dep["name"] for dep in pkg.get("dependencies", [])],
                    "features": list(pkg.get("features", {}).keys()),
                }
                for pkg in packages
            ],
            "workspace_members": workspace_members,
        }
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as e:
        return {"error": str(e), "is_workspace": False}


def detect_architecture_style(project_path: Path) -> list[dict[str, Any]]:
    """Detect architectural patterns used in a project.
    
    Filters out test/bench/example code to reduce false positives.
    """
    detected = []
    workspace_info = analyze_workspace(project_path)
    
    # Collect production Rust source code (excludes tests/benches/examples)
    all_code = ""
    for rs_file in _iter_source_files(project_path, include_tests=False):
        try:
            all_code += rs_file.read_text() + "\n"
        except Exception:
            continue
    
    # Also check Cargo.toml for dependencies
    cargo_toml = project_path / "Cargo.toml"
    cargo_content = ""
    if cargo_toml.exists():
        try:
            cargo_content = cargo_toml.read_text()
        except Exception:
            pass
    
    combined_content = all_code + cargo_content
    
    # Check for workspace-based architecture
    if workspace_info.get("is_workspace") and workspace_info.get("package_count", 0) > 3:
        detected.append({
            "style": "Multi-Crate Workspace",
            "confidence": 0.9,
            "evidence": [f"Workspace with {workspace_info['package_count']} packages"],
            "description": ARCHITECTURE_STYLES["Multi-Crate Workspace"]["description"],
        })
    elif not workspace_info.get("is_workspace"):
        # Check if it's a modular monolith
        module_count = all_code.count("mod ") + all_code.count("pub mod ")
        if module_count > 10:
            detected.append({
                "style": "Modular Monolith",
                "confidence": 0.7,
                "evidence": [f"Single crate with {module_count}+ module declarations"],
                "description": ARCHITECTURE_STYLES["Modular Monolith"]["description"],
            })
    
    # Check for other patterns
    for style_name, style_info in ARCHITECTURE_STYLES.items():
        if style_name in ["Modular Monolith", "Multi-Crate Workspace"]:
            continue  # Already checked above
        
        indicators = style_info["indicators"]
        found_indicators = []
        for indicator in indicators:
            if indicator in combined_content:
                found_indicators.append(indicator)
        
        if found_indicators:
            confidence = len(found_indicators) / len(indicators)
            if confidence >= 0.3:  # Threshold
                detected.append({
                    "style": style_name,
                    "confidence": confidence,
                    "evidence": found_indicators,
                    "description": style_info["description"],
                })
    
    # Sort by confidence
    detected.sort(key=lambda x: x["confidence"], reverse=True)
    return detected


def detect_communication_patterns(project_path: Path) -> list[dict[str, Any]]:
    """Detect communication patterns between components.
    
    Filters out test/bench/example code to reduce false positives.
    """
    detected = []
    
    # Collect production Rust source code (excludes tests/benches/examples)
    all_code = ""
    for rs_file in _iter_source_files(project_path, include_tests=False):
        try:
            all_code += rs_file.read_text() + "\n"
        except Exception:
            continue
    
    # Check Cargo.toml for dependencies
    cargo_toml = project_path / "Cargo.toml"
    cargo_content = ""
    if cargo_toml.exists():
        try:
            cargo_content = cargo_toml.read_text()
        except Exception:
            pass
    
    combined = all_code + cargo_content
    
    for pattern_name, signatures in COMMUNICATION_PATTERNS.items():
        found = []
        for sig in signatures:
            if sig in combined:
                found.append(sig)
        
        if found:
            detected.append({
                "pattern": pattern_name,
                "evidence": found,
                "usage_count": sum(combined.count(sig) for sig in found),
            })
    
    detected.sort(key=lambda x: x["usage_count"], reverse=True)
    return detected


def generate_c4_context(project_path: Path, project_name: str | None = None) -> str:
    """Generate C4 Context diagram in Mermaid format."""
    if project_name is None:
        project_name = project_path.name
    
    workspace = analyze_workspace(project_path)
    styles = detect_architecture_style(project_path)
    
    # Build Mermaid diagram
    lines = [
        "```mermaid",
        "C4Context",
        f'title System Context Diagram for {project_name}',
        "",
        f'System({project_name.lower()}, "{project_name}", "Rust Application")',
    ]
    
    # Add external systems based on dependencies
    if workspace.get("packages"):
        external_deps = set()
        for pkg in workspace["packages"]:
            for dep in pkg.get("dependencies", []):
                if dep not in [p["name"] for p in workspace["packages"]]:
                    external_deps.add(dep)
        
        # Add notable external dependencies
        notable = ["tokio", "actix", "axum", "hyper", "serde", "diesel", "sqlx", "redis", "kafka"]
        for dep in external_deps:
            if any(n in dep.lower() for n in notable):
                lines.append(f'System_Ext({dep.replace("-", "_")}, "{dep}", "External Crate")')
    
    lines.append("```")
    return "\n".join(lines)


def generate_c4_container(project_path: Path, project_name: str | None = None) -> str:
    """Generate C4 Container diagram in Mermaid format.
    
    Improvements:
    - Filters out test/bench/example crates
    - Categorizes core vs auxiliary packages
    - Better description handling
    """
    if project_name is None:
        project_name = project_path.name
    
    workspace = analyze_workspace(project_path)
    
    lines = [
        "```mermaid",
        "C4Container",
        f'title Container Diagram for {project_name}',
        "",
        f'System_Boundary({project_name.lower().replace("-", "_")}_boundary, "{project_name}") {{',
    ]
    
    if workspace.get("packages"):
        # Categorize packages
        core_packages = []
        aux_packages = []
        
        test_patterns = ["test", "bench", "example", "stress", "fuzz"]
        
        for pkg in workspace["packages"]:
            pkg_name = pkg["name"]
            pkg_lower = pkg_name.lower()
            
            # Filter out test/bench/example crates
            is_test_crate = any(pattern in pkg_lower for pattern in test_patterns)
            
            if is_test_crate:
                continue  # Skip test crates from main diagram
            
            # Consider core if has description or is main crate
            has_desc = bool(pkg.get("description"))
            is_main = pkg_name == project_name or pkg_name.startswith(f"{project_name}-")
            
            if is_main or has_desc:
                core_packages.append(pkg)
            else:
                aux_packages.append(pkg)
        
        # Add core packages first
        for pkg in core_packages[:10]:
            pkg_name = pkg["name"]
            pkg_desc = pkg.get("description", "")
            
            # Clean and truncate description
            if pkg_desc:
                # Remove newlines and extra whitespace
                pkg_desc = " ".join(pkg_desc.split())
                # Truncate intelligently at word boundary
                if len(pkg_desc) > 60:
                    pkg_desc = pkg_desc[:57].rsplit(" ", 1)[0] + "..."
            else:
                pkg_desc = f"{pkg_name} crate"
            
            safe_name = pkg_name.replace("-", "_")
            lines.append(f'    Container({safe_name}, "{pkg_name}", "Rust", "{pkg_desc}")')
        
        # Add note about auxiliary packages if any
        if aux_packages and len(aux_packages) <= 5:
            for pkg in aux_packages:
                pkg_name = pkg["name"]
                safe_name = pkg_name.replace("-", "_")
                lines.append(f'    Container({safe_name}, "{pkg_name}", "Rust", "Internal crate")')
        elif aux_packages:
            lines.append(f'    %% {len(aux_packages)} additional internal crates not shown')
    else:
        lines.append(f'    Container(main, "{project_name}", "Rust", "Main application")')
    
    lines.append("}")
    lines.append("```")
    return "\n".join(lines)


def generate_c4_component(project_path: Path, crate_name: str | None = None) -> str:
    """Generate C4 Component diagram for a specific crate."""
    if crate_name is None:
        crate_name = project_path.name
    
    # Find main modules in src
    src_path = project_path / "src"
    if not src_path.exists():
        return "No src directory found"
    
    lines = [
        "```mermaid",
        "C4Component",
        f'title Component Diagram for {crate_name}',
        "",
        f'Container_Boundary({crate_name.replace("-", "_")}_boundary, "{crate_name}") {{',
    ]
    
    # Find module directories and files
    modules = []
    for item in src_path.iterdir():
        if item.is_dir() and not item.name.startswith("_"):
            modules.append(item.name)
        elif item.suffix == ".rs" and item.stem not in ["lib", "main", "mod"]:
            modules.append(item.stem)
    
    for mod in modules[:10]:  # Limit to 10 modules
        safe_name = mod.replace("-", "_")
        lines.append(f'    Component({safe_name}, "{mod}", "Module", "Rust module")')
    
    lines.append("}")
    lines.append("```")
    return "\n".join(lines)


def analyze(project_path: Path, include_dynamic: bool = True) -> dict[str, Any]:
    """Full architecture analysis of a project.
    
    Args:
        project_path: Path to the Rust project
        include_dynamic: Include dynamic analysis (tracing)
    """
    result = {
        "workspace": analyze_workspace(project_path),
        "architecture_styles": detect_architecture_style(project_path),
        "communication_patterns": detect_communication_patterns(project_path),
    }
    
    if include_dynamic:
        from rust_asr.analysis.dynamic import tracing
        result["tracing"] = tracing.detect_tracing_usage(project_path)
    
    return result


def export_report(analysis: dict[str, Any], output: Path, project_name: str | None = None) -> None:
    """Export architecture analysis as markdown report."""
    if project_name is None:
        project_name = "Project"
    
    lines = [
        f"# System Architecture Analysis: {project_name}",
        "",
    ]
    
    # Workspace info
    ws = analysis.get("workspace", {})
    if ws.get("is_workspace"):
        lines.extend([
            "## Workspace Structure",
            "",
            f"- **Type:** Multi-crate workspace",
            f"- **Package count:** {ws.get('package_count', 0)}",
            "",
            "### Packages",
            "",
        ])
        for pkg in ws.get("packages", []):
            lines.append(f"- **{pkg['name']}** v{pkg['version']}")
            if pkg.get("description"):
                lines.append(f"  - {pkg['description']}")
            if pkg.get("features"):
                lines.append(f"  - Features: {', '.join(pkg['features'][:5])}")
        lines.append("")
    
    # Architecture styles
    styles = analysis.get("architecture_styles", [])
    if styles:
        lines.extend([
            "## Detected Architecture Styles",
            "",
        ])
        for style in styles:
            lines.append(f"### {style['style']}")
            lines.append(f"**Confidence:** {style['confidence']:.0%}")
            lines.append(f"**Description:** {style['description']}")
            lines.append("")
            lines.append("**Evidence:**")
            for e in style["evidence"][:5]:
                lines.append(f"- {e}")
            lines.append("")
    
    # Communication patterns
    patterns = analysis.get("communication_patterns", [])
    if patterns:
        lines.extend([
            "## Communication Patterns",
            "",
        ])
        for p in patterns:
            lines.append(f"- **{p['pattern']}** (found {p['usage_count']} usages)")
        lines.append("")
    
    # Dynamic analysis - tracing
    tracing = analysis.get("tracing", {})
    if tracing.get("uses_tracing") or tracing.get("instrumented_count", 0) > 0:
        lines.extend([
            "## Runtime Observability",
            "",
            f"- **Uses `tracing`:** {'✅' if tracing.get('uses_tracing') else '❌'}",
            f"- **Uses tokio tracing:** {'✅' if tracing.get('uses_tokio_tracing') else '❌'}",
            f"- **Instrumented functions:** {tracing.get('instrumented_count', 0)}",
            "",
        ])
        
        if tracing.get("instrumented_functions"):
            lines.append("### Top Instrumented Functions")
            lines.append("")
            lines.append("| Function | File |")
            lines.append("|----------|------|")
            for f in tracing.get("instrumented_functions", [])[:10]:
                lines.append(f"| `{f['function']}` | {f['file']} |")
            lines.append("")
    
    output.write_text("\n".join(lines))

