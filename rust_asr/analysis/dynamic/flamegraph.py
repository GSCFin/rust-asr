"""Flamegraph generation wrapper for Rust projects."""

import subprocess
import shutil
from pathlib import Path
from typing import Any

from rich.console import Console

console = Console()


def check_prerequisites() -> dict[str, bool]:
    """Check if flamegraph tools are installed."""
    tools = {
        "cargo-flamegraph": shutil.which("cargo-flamegraph") is not None,
        "perf": shutil.which("perf") is not None,  # Linux
        "dtrace": shutil.which("dtrace") is not None,  # macOS
        "inferno": shutil.which("inferno-flamegraph") is not None,
    }
    return tools


def generate(
    project_path: Path,
    output_path: Path,
    binary: str | None = None,
    release: bool = True,
) -> dict[str, Any]:
    """Generate flamegraph for a Rust project.
    
    Args:
        project_path: Path to the Rust project
        output_path: Where to save the flamegraph SVG
        binary: Specific binary to profile (defaults to main)
        release: Build in release mode for accurate profiling
    
    Returns:
        dict with success status and paths
    """
    result = {
        "success": False,
        "svg_path": None,
        "error": None,
    }
    
    # Check prerequisites
    prereqs = check_prerequisites()
    if not prereqs["cargo-flamegraph"]:
        result["error"] = "cargo-flamegraph not installed. Run: cargo install flamegraph"
        return result
    
    output_path.mkdir(parents=True, exist_ok=True)
    svg_file = output_path / f"{project_path.name}_flamegraph.svg"
    
    cmd = ["cargo", "flamegraph", "-o", str(svg_file)]
    
    if release:
        cmd.append("--release")
    
    if binary:
        cmd.extend(["--bin", binary])
    
    try:
        proc = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes max
        )
        
        if proc.returncode == 0 and svg_file.exists():
            result["success"] = True
            result["svg_path"] = str(svg_file)
        else:
            result["error"] = proc.stderr[:500] if proc.stderr else "Unknown error"
            
    except subprocess.TimeoutExpired:
        result["error"] = "Flamegraph generation timed out"
    except FileNotFoundError:
        result["error"] = "cargo-flamegraph not found"
    except Exception as e:
        result["error"] = str(e)
    
    return result


def analyze_hotspots(svg_path: Path) -> list[dict[str, Any]]:
    """Parse flamegraph SVG to extract hot functions.
    
    Note: This is a simplified parser. For production use,
    consider using the inferno-flamegraph JSON output.
    """
    hotspots = []
    
    if not svg_path.exists():
        return hotspots
    
    try:
        content = svg_path.read_text()
        
        # Simple regex to find function names and widths
        import re
        
        # Look for rect elements with title (function name)
        pattern = r'<title>([^<]+)</title>\s*<rect[^>]*width="([0-9.]+)"'
        
        for match in re.finditer(pattern, content):
            func_name = match.group(1)
            width = float(match.group(2))
            
            # Filter out very small items
            if width > 10:
                hotspots.append({
                    "function": func_name.split(";")[-1] if ";" in func_name else func_name,
                    "width": width,
                    "full_path": func_name,
                })
        
        # Sort by width (hottest first)
        hotspots.sort(key=lambda x: x["width"], reverse=True)
        
    except Exception:
        pass
    
    return hotspots[:20]  # Top 20 hotspots


def format_report(hotspots: list[dict[str, Any]], output: Path) -> None:
    """Generate markdown report from hotspots."""
    lines = [
        "# Flamegraph Analysis",
        "",
        "## Top Hot Functions",
        "",
        "| Function | Relative Width |",
        "|----------|----------------|",
    ]
    
    for h in hotspots[:15]:
        lines.append(f"| `{h['function'][:50]}` | {h['width']:.1f} |")
    
    output.write_text("\n".join(lines))
