"""Analyze command - Full architecture analysis of a Rust project."""

import os
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def execute(path: str | None, repo: str | None, output: str) -> None:
    """Execute full architecture analysis."""
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Step 1: Resolve project path
        if repo:
            from rust_asr.repos import fetcher
            task = progress.add_task("Cloning repository...", total=None)
            project_path = fetcher.clone_repo(repo, Path("repos"))
            progress.remove_task(task)
        else:
            project_path = Path(path)  # type: ignore
        
        console.print(f"[green]✓[/green] Analyzing: {project_path.name}")
        
        # Step 2: Dependency analysis
        task = progress.add_task("Analyzing dependencies...", total=None)
        from rust_asr.analysis import dependency
        dep_graph = dependency.analyze(project_path)
        dep_output = output_path / "dependencies.md"
        dependency.export_mermaid(dep_graph, dep_output)
        progress.remove_task(task)
        console.print(f"[green]✓[/green] Dependencies: {dep_output}")
        
        # Step 3: Module structure
        task = progress.add_task("Analyzing modules...", total=None)
        from rust_asr.analysis import modules
        mod_tree = modules.analyze(project_path)
        mod_output = output_path / "modules.md"
        modules.export_tree(mod_tree, mod_output)
        progress.remove_task(task)
        console.print(f"[green]✓[/green] Modules: {mod_output}")
        
        # Step 4: Metrics
        task = progress.add_task("Collecting metrics...", total=None)
        from rust_asr.analysis import metrics
        stats = metrics.analyze(project_path)
        metrics_output = output_path / "metrics.json"
        metrics.export_json(stats, metrics_output)
        progress.remove_task(task)
        console.print(f"[green]✓[/green] Metrics: {metrics_output}")
        
        # Step 5: Pattern detection
        task = progress.add_task("Detecting patterns...", total=None)
        from rust_asr.analysis import patterns
        detected = patterns.analyze(project_path)
        patterns_output = output_path / "patterns.md"
        patterns.export_report(detected, patterns_output)
        progress.remove_task(task)
        console.print(f"[green]✓[/green] Patterns: {patterns_output}")
        
        # Step 6: Generate summary
        summary_output = output_path / "SUMMARY.md"
        _generate_summary(project_path, dep_graph, mod_tree, stats, detected, summary_output)
        console.print(f"[green]✓[/green] Summary: {summary_output}")
    
    console.print(f"\n[bold green]Analysis complete![/bold green] Results in: {output_path}")


def _generate_summary(
    project_path: Path,
    dep_graph: dict,
    mod_tree: dict,
    stats: dict,
    patterns: list,
    output: Path,
) -> None:
    """Generate analysis summary markdown."""
    content = f"""# Architecture Analysis: {project_path.name}

## Overview

| Metric | Value |
|--------|-------|
| Total Lines | {stats.get('lines', 'N/A')} |
| Rust Files | {stats.get('rust_files', 'N/A')} |
| Crates | {len(dep_graph.get('nodes', []))} |
| Core Components | {len([n for n in dep_graph.get('nodes', []) if n.get('in_degree', 0) > 3])} |

## Detected Patterns

{chr(10).join([f"- {p}" for p in patterns]) if patterns else "No patterns detected."}

## Key Components

See `dependencies.md` for full dependency graph.

## Module Structure

See `modules.md` for full module tree.
"""
    output.write_text(content)
