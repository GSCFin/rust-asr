"""Critical Paths documentation export module.

Generates 04-critical-paths/ documentation:
- main-flows.md: Core use cases
- error-handling.md: Error strategy
- performance-hotspots.md: From flamegraph/tracing
"""

from pathlib import Path
from typing import Any
import re


def analyze_error_handling(project_path: Path) -> dict[str, Any]:
    """Analyze error handling patterns in Rust source files."""
    error_info = {
        "uses_anyhow": False,
        "uses_thiserror": False,
        "custom_errors": [],
        "result_returns": 0,
        "unwrap_calls": 0,
        "expect_calls": 0,
        "question_marks": 0,
    }
    
    src_path = project_path / "src"
    if not src_path.exists():
        src_path = project_path
    
    error_enum_pattern = re.compile(r"(?:#\[derive\([^)]*Error[^)]*\)\]|\s*enum\s+\w*Error)", re.MULTILINE)
    result_pattern = re.compile(r"->\s*(?:anyhow::|crate::)?Result<", re.MULTILINE)
    unwrap_pattern = re.compile(r"\.unwrap\(\)", re.MULTILINE)
    expect_pattern = re.compile(r"\.expect\(", re.MULTILINE)
    question_pattern = re.compile(r"\?\s*;|\?\s*\)", re.MULTILINE)
    
    for rs_file in src_path.rglob("*.rs"):
        try:
            content = rs_file.read_text(errors="ignore")
            rel_path = rs_file.relative_to(project_path)
            
            if "anyhow::" in content or "use anyhow" in content:
                error_info["uses_anyhow"] = True
            
            if "thiserror" in content:
                error_info["uses_thiserror"] = True
            
            for match in error_enum_pattern.finditer(content):
                error_info["custom_errors"].append(str(rel_path))
            
            error_info["result_returns"] += len(result_pattern.findall(content))
            error_info["unwrap_calls"] += len(unwrap_pattern.findall(content))
            error_info["expect_calls"] += len(expect_pattern.findall(content))
            error_info["question_marks"] += len(question_pattern.findall(content))
            
        except Exception:
            continue
    
    return error_info


def generate_main_flows(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate main-flows.md with core use cases."""
    project_name = project_path.name
    comm_patterns = analysis.get("communication_patterns", [])
    patterns = analysis.get("patterns", [])
    tracing_info = analysis.get("tracing", {})
    
    lines = [
        f"# Main Flows: {project_name}",
        "",
        "## Core Use Cases",
        "",
        "```mermaid",
        "graph TD",
        "    A[User Input] --> B[Validate]",
        "    B --> C{Valid?}",
        "    C -->|Yes| D[Process]",
        "    C -->|No| E[Error Response]",
        "    D --> F[Output Result]",
        "    E --> G[Return Error]",
        "```",
        "",
        "## Processing Pipeline",
        "",
    ]
    
    # Build flow from detected patterns
    if comm_patterns:
        lines.extend([
            "| Step | Pattern | Description |",
            "|------|---------|-------------|",
        ])
        for i, pattern in enumerate(comm_patterns[:5], 1):
            lines.append(f"| {i} | {pattern['pattern']} | Inter-component communication |")
    else:
        lines.extend([
            "| Step | Description |",
            "|------|-------------|",
            "| 1 | Input parsing |",
            "| 2 | Validation |",
            "| 3 | Core processing |",
            "| 4 | Output generation |",
        ])
    
    # Instrumented hot paths
    if tracing_info.get("instrumented_functions"):
        lines.extend([
            "",
            "## Instrumented Entry Points",
            "",
            "Functions with `#[instrument]` tracking:",
            "",
        ])
        for fn in tracing_info["instrumented_functions"][:8]:
            lines.append(f"- `{fn['function']}` in {fn['file']}")
    
    return "\n".join(lines)


def generate_error_handling(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate error-handling.md with error strategy."""
    project_name = project_path.name
    error_info = analyze_error_handling(project_path)
    
    lines = [
        f"# Error Handling: {project_name}",
        "",
        "## Error Strategy Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Uses `anyhow` | {'✅' if error_info['uses_anyhow'] else '❌'} |",
        f"| Uses `thiserror` | {'✅' if error_info['uses_thiserror'] else '❌'} |",
        f"| Result returns | {error_info['result_returns']} |",
        f"| `?` operator usage | {error_info['question_marks']} |",
        f"| `.unwrap()` calls | {error_info['unwrap_calls']} |",
        f"| `.expect()` calls | {error_info['expect_calls']} |",
        "",
    ]
    
    # Error handling assessment
    total_unsafe = error_info["unwrap_calls"] + error_info["expect_calls"]
    total_safe = error_info["question_marks"]
    
    if total_safe > total_unsafe * 3:
        assessment = "✅ **Good**: Mostly uses `?` operator for error propagation"
    elif total_unsafe > total_safe:
        assessment = "⚠️ **Warning**: High usage of `.unwrap()/.expect()` may cause panics"
    else:
        assessment = "📊 **Mixed**: Uses a combination of approaches"
    
    lines.extend([
        "## Assessment",
        "",
        assessment,
        "",
    ])
    
    # Error hierarchy
    lines.extend([
        "## Error Propagation Pattern",
        "",
        "```mermaid",
        "graph TD",
        "    A[Operation] -->|Result| B{Ok/Err}",
        "    B -->|Ok| C[Continue]",
        "    B -->|Err| D[? Operator]",
        "    D --> E[Propagate Up]",
        "```",
    ])
    
    # Custom errors
    if error_info["custom_errors"]:
        lines.extend([
            "",
            "## Custom Error Types",
            "",
        ])
        unique_files = list(set(error_info["custom_errors"]))[:5]
        for f in unique_files:
            lines.append(f"- `{f}`")
    
    return "\n".join(lines)


def generate_performance_hotspots(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate performance-hotspots.md from tracing/flamegraph."""
    project_name = project_path.name
    tracing_info = analysis.get("tracing", {})
    
    lines = [
        f"# Performance Hotspots: {project_name}",
        "",
        "## Observability Status",
        "",
        f"- **Tracing enabled**: {'✅' if tracing_info.get('uses_tracing') else '❌'} ",
        f"- **Tokio tracing**: {'✅' if tracing_info.get('uses_tokio_tracing') else '❌'}",
        f"- **Instrumented functions**: {tracing_info.get('instrumented_count', 0)}",
        "",
    ]
    
    if tracing_info.get("instrumented_functions"):
        lines.extend([
            "## Instrumented Functions",
            "",
            "| Function | File | Notes |",
            "|----------|------|-------|",
        ])
        for fn in tracing_info["instrumented_functions"][:15]:
            lines.append(f"| `{fn['function']}` | {fn['file']} | Traced |")
    else:
        lines.extend([
            "## Recommendations",
            "",
            "No instrumented functions detected. Consider adding:",
            "",
            "```rust",
            '#[tracing::instrument]',
            "pub fn critical_function() {",
            "    // ...",
            "}",
            "```",
        ])
    
    # Flamegraph guidance
    lines.extend([
        "",
        "## Flamegraph Analysis",
        "",
        "To generate flamegraph for runtime analysis:",
        "",
        "```bash",
        "cargo install flamegraph",
        f"cargo flamegraph --bin {project_name}",
        "```",
        "",
        "> Generated flamegraph.svg can reveal CPU hotspots.",
    ])
    
    return "\n".join(lines)


def export_critical_paths(
    project_path: Path,
    output_dir: Path,
    analysis: dict[str, Any],
) -> dict[str, Path]:
    """Export 04-critical-paths/ documentation.
    
    Args:
        project_path: Path to Rust project
        output_dir: Output directory
        analysis: Complete analysis data
        
    Returns:
        Dict mapping file names to paths
    """
    paths_dir = Path(output_dir) / "04-critical-paths"
    paths_dir.mkdir(parents=True, exist_ok=True)
    
    files = {}
    
    # main-flows.md
    content = generate_main_flows(project_path, analysis)
    path = paths_dir / "main-flows.md"
    path.write_text(content)
    files["main-flows.md"] = path
    
    # error-handling.md
    content = generate_error_handling(project_path, analysis)
    path = paths_dir / "error-handling.md"
    path.write_text(content)
    files["error-handling.md"] = path
    
    # performance-hotspots.md
    content = generate_performance_hotspots(project_path, analysis)
    path = paths_dir / "performance-hotspots.md"
    path.write_text(content)
    files["performance-hotspots.md"] = path
    
    return files
