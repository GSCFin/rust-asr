"""LLM Context Export - Full codebase dump using repomix."""

import re
import subprocess
import shutil
from pathlib import Path
from typing import Any


def export_full_context(
    project_path: Path,
    output_dir: Path,
    chunk_size: str = "2mb",
    max_lines_fallback: int = 20000,
) -> dict[str, Any]:
    """
    Export full codebase using repomix with smart splitting.
    
    Args:
        project_path: Path to Rust project
        output_dir: Output directory for codebase files
        chunk_size: Size per chunk for repomix (e.g., "2mb", "500kb")
        max_lines_fallback: Max lines per file if manual split needed
    
    Returns:
        dict with: files_created, total_lines, total_size, method
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    base_name = "codebase"
    output_file = output_dir / f"{base_name}.txt"
    
    if not _check_repomix_available():
        return _fallback_simple_export(project_path, output_dir, base_name)
    
    success, split_files = _run_repomix_with_split(
        project_path, output_dir, base_name, chunk_size
    )
    
    if success and split_files:
        return _collect_result(split_files, method="repomix_split")
    
    success = _run_repomix_no_split(project_path, output_file)
    
    if not success or not output_file.exists():
        return _fallback_simple_export(project_path, output_dir, base_name)
    
    lines = output_file.read_text(errors="ignore").count("\n")
    
    if lines > max_lines_fallback:
        split_files = manual_split_codebase(output_file, output_dir, max_lines_fallback)
        output_file.unlink(missing_ok=True)
        return _collect_result(split_files, method="manual_split")
    
    return _collect_result([output_file], method="repomix_single")


def _check_repomix_available() -> bool:
    """Check if repomix CLI is available."""
    return shutil.which("repomix") is not None or shutil.which("npx") is not None


def _run_repomix_with_split(
    project_path: Path,
    output_dir: Path,
    base_name: str,
    chunk_size: str,
) -> tuple[bool, list[Path]]:
    """Run repomix with --split-output option."""
    output_file = output_dir / f"{base_name}.txt"
    
    cmd = [
        "repomix" if shutil.which("repomix") else "npx",
    ]
    if "npx" in cmd[0]:
        cmd.append("repomix")
    
    cmd.extend([
        "--style", "plain",
        "--compress",
        "--remove-comments",
        "--remove-empty-lines",
        "--output", str(output_file),
        "--split-output", chunk_size,
        str(project_path),
    ])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        
        if "Cannot split output" in result.stderr:
            return False, []
        
        split_pattern = f"{base_name}.[0-9]*.txt"
        split_files = sorted(output_dir.glob(split_pattern))
        
        if split_files:
            return True, split_files
        elif output_file.exists():
            return True, [output_file]
        
        return result.returncode == 0, []
        
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, []


def _run_repomix_no_split(project_path: Path, output_file: Path) -> bool:
    """Run repomix without splitting."""
    cmd = [
        "repomix" if shutil.which("repomix") else "npx",
    ]
    if "npx" in cmd[0]:
        cmd.append("repomix")
    
    cmd.extend([
        "--style", "plain",
        "--compress",
        "--remove-comments", 
        "--remove-empty-lines",
        "--output", str(output_file),
        str(project_path),
    ])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def manual_split_codebase(
    input_file: Path,
    output_dir: Path,
    max_lines: int = 20000,
) -> list[Path]:
    """
    Fallback: Manual split when repomix --split-output fails.
    
    Splits at file boundaries (pattern: "================\\nFile: ...\\n================")
    to ensure each chunk is semantically complete.
    """
    content = input_file.read_text(errors="ignore")
    
    pattern = r"(^={16,}\nFile: .+\n={16,})"
    sections = re.split(pattern, content, flags=re.MULTILINE)
    
    header = sections[0] if sections else ""
    
    file_sections = []
    i = 1
    while i < len(sections):
        if i + 1 < len(sections):
            file_sections.append(sections[i] + sections[i + 1])
        else:
            file_sections.append(sections[i])
        i += 2
    
    parts: list[str] = []
    current_part = header
    current_lines = header.count("\n")
    
    for section in file_sections:
        section_lines = section.count("\n")
        
        if current_lines + section_lines > max_lines and current_lines > 0:
            parts.append(current_part)
            current_part = header + section
            current_lines = header.count("\n") + section_lines
        else:
            current_part += section
            current_lines += section_lines
    
    if current_part:
        parts.append(current_part)
    
    base_name = input_file.stem
    output_files: list[Path] = []
    
    for idx, part in enumerate(parts, 1):
        out_file = output_dir / f"{base_name}.{idx}.txt"
        out_file.write_text(part)
        output_files.append(out_file)
    
    return output_files


def _fallback_simple_export(
    project_path: Path,
    output_dir: Path,
    base_name: str,
) -> dict[str, Any]:
    """Simple fallback: concatenate all .rs files."""
    output_file = output_dir / f"{base_name}.txt"
    
    lines = [f"# Codebase: {project_path.name}", ""]
    
    priority_files = ["Cargo.toml", "src/lib.rs", "src/main.rs", "README.md"]
    for pf in priority_files:
        file_path = project_path / pf
        if file_path.exists():
            lines.append(f"=" * 20)
            lines.append(f"File: {pf}")
            lines.append(f"=" * 20)
            try:
                lines.append(file_path.read_text(errors="ignore"))
            except Exception:
                lines.append("(Error reading file)")
            lines.append("")
    
    for rs_file in sorted(project_path.rglob("*.rs")):
        if "target" in rs_file.parts:
            continue
        rel_path = rs_file.relative_to(project_path)
        lines.append(f"=" * 20)
        lines.append(f"File: {rel_path}")
        lines.append(f"=" * 20)
        try:
            lines.append(rs_file.read_text(errors="ignore"))
        except Exception:
            lines.append("(Error reading file)")
        lines.append("")
    
    content = "\n".join(lines)
    output_file.write_text(content)
    
    return _collect_result([output_file], method="fallback_simple")


def _collect_result(files: list[Path], method: str) -> dict[str, Any]:
    """Collect export result metadata."""
    total_lines = 0
    total_size = 0
    
    for f in files:
        if f.exists():
            content = f.read_text(errors="ignore")
            total_lines += content.count("\n")
            total_size += f.stat().st_size
    
    return {
        "files_created": [str(f) for f in files],
        "file_count": len(files),
        "total_lines": total_lines,
        "total_size": total_size,
        "method": method,
    }
