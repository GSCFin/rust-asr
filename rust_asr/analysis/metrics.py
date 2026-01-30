"""Code metrics analysis using tokei and other tools."""

import subprocess
import json
from pathlib import Path
from typing import Any


def analyze(project_path: Path) -> dict[str, Any]:
    """Collect code metrics for a project."""
    stats = {
        "lines": 0,
        "code": 0,
        "comments": 0,
        "blanks": 0,
        "rust_files": 0,
    }
    
    # Try tokei first (most accurate)
    try:
        result = subprocess.run(
            ["tokei", "--output", "json", str(project_path)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            
            # Extract Rust stats
            rust_data = data.get("Rust", data.get("rust", {}))
            if rust_data:
                stats["lines"] = rust_data.get("lines", 0)
                stats["code"] = rust_data.get("code", 0)
                stats["comments"] = rust_data.get("comments", 0)
                stats["blanks"] = rust_data.get("blanks", 0)
                reports = rust_data.get("reports", rust_data.get("children", {}))
                if isinstance(reports, list):
                    stats["rust_files"] = len(reports)
                elif isinstance(reports, dict):
                    stats["rust_files"] = len(reports)
            
            return stats
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass
    
    # Fallback: manual counting
    return _manual_count(project_path)


def _manual_count(project_path: Path) -> dict[str, Any]:
    """Manually count lines in Rust files."""
    stats = {
        "lines": 0,
        "code": 0,
        "comments": 0,
        "blanks": 0,
        "rust_files": 0,
    }
    
    src_path = project_path / "src"
    if not src_path.exists():
        src_path = project_path
    
    for rs_file in src_path.rglob("*.rs"):
        stats["rust_files"] += 1
        
        try:
            content = rs_file.read_text()
            lines = content.split("\n")
            
            for line in lines:
                stripped = line.strip()
                stats["lines"] += 1
                
                if not stripped:
                    stats["blanks"] += 1
                elif stripped.startswith("//") or stripped.startswith("/*"):
                    stats["comments"] += 1
                else:
                    stats["code"] += 1
        except Exception:
            continue
    
    return stats


def export_json(stats: dict[str, Any], output: Path) -> None:
    """Export metrics as JSON."""
    output.write_text(json.dumps(stats, indent=2))
