"""Tracing and tokio-console integration for async analysis."""

import subprocess
import json
import re
from pathlib import Path
from typing import Any


def check_prerequisites() -> dict[str, bool]:
    """Check if tracing tools are installed."""
    import shutil
    
    return {
        "tokio-console": shutil.which("tokio-console") is not None,
        "tracing-subscriber": True,  # Usually a crate dependency
    }


def detect_tracing_usage(project_path: Path) -> dict[str, Any]:
    """Detect how a project uses the tracing ecosystem."""
    result = {
        "uses_tracing": False,
        "uses_tokio_tracing": False,
        "subscriber_config": None,
        "span_patterns": [],
        "instrumented_functions": [],
    }
    
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        content = cargo_toml.read_text()
        result["uses_tracing"] = "tracing" in content
        result["uses_tokio_tracing"] = "tokio" in content and "tracing" in content
    
    # Scan source for tracing patterns
    src_path = project_path / "src"
    if not src_path.exists():
        return result
    
    span_pattern = re.compile(r'#\[instrument[^\]]*\]')
    event_pattern = re.compile(r'(tracing::|log::)?(info|debug|warn|error|trace)!')
    
    for rs_file in src_path.rglob("*.rs"):
        try:
            content = rs_file.read_text()
            
            # Find instrumented functions
            for match in span_pattern.finditer(content):
                # Get the function name after the attribute
                pos = match.end()
                func_match = re.search(r'fn\s+(\w+)', content[pos:pos+100])
                if func_match:
                    result["instrumented_functions"].append({
                        "function": func_match.group(1),
                        "file": str(rs_file.relative_to(project_path)),
                    })
            
            # Count event macros
            events = event_pattern.findall(content)
            if events:
                result["span_patterns"].extend([e[1] for e in events])
                
        except Exception:
            continue
    
    # Summarize
    result["span_patterns"] = list(set(result["span_patterns"]))
    result["instrumented_count"] = len(result["instrumented_functions"])
    
    return result


def parse_tokio_console_dump(dump_path: Path) -> dict[str, Any]:
    """Parse tokio-console JSON dump for async task analysis."""
    result = {
        "tasks": [],
        "resources": [],
        "task_stats": {},
    }
    
    if not dump_path.exists():
        return result
    
    try:
        data = json.loads(dump_path.read_text())
        
        # Extract task information
        for task in data.get("tasks", []):
            result["tasks"].append({
                "id": task.get("id"),
                "name": task.get("name", "unnamed"),
                "state": task.get("state"),
                "polls": task.get("total_polls", 0),
                "busy_time": task.get("busy", 0),
                "idle_time": task.get("idle", 0),
            })
        
        # Calculate stats
        if result["tasks"]:
            total_polls = sum(t["polls"] for t in result["tasks"])
            result["task_stats"] = {
                "total_tasks": len(result["tasks"]),
                "total_polls": total_polls,
                "avg_polls": total_polls / len(result["tasks"]),
            }
            
    except Exception:
        pass
    
    return result


def generate_async_report(project_path: Path, output: Path) -> None:
    """Generate async analysis report."""
    tracing_info = detect_tracing_usage(project_path)
    
    lines = [
        "# Async Analysis Report",
        "",
        "## Tracing Configuration",
        "",
        f"- Uses `tracing`: {'✅' if tracing_info['uses_tracing'] else '❌'}",
        f"- Uses tokio tracing: {'✅' if tracing_info['uses_tokio_tracing'] else '❌'}",
        f"- Instrumented functions: {tracing_info.get('instrumented_count', 0)}",
        "",
    ]
    
    if tracing_info["instrumented_functions"]:
        lines.append("## Instrumented Functions")
        lines.append("")
        lines.append("| Function | File |")
        lines.append("|----------|------|")
        for f in tracing_info["instrumented_functions"][:20]:
            lines.append(f"| `{f['function']}` | {f['file']} |")
        lines.append("")
    
    if tracing_info["span_patterns"]:
        lines.append("## Event Levels Used")
        lines.append("")
        for level in tracing_info["span_patterns"]:
            lines.append(f"- `{level}!`")
    
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines))
