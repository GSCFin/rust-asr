"""Patterns command - Detect architectural patterns."""

from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()


def execute(path: str) -> None:
    """Detect architectural patterns in a project."""
    from rust_asr.analysis import patterns
    
    project_path = Path(path)
    
    console.print(f"[cyan]Detecting patterns: {project_path.name}[/cyan]")
    
    # Run analysis
    detected = patterns.analyze(project_path)
    
    if not detected:
        console.print("[yellow]No architectural patterns detected.[/yellow]")
        return
    
    # Display results
    table = Table(title="Detected Patterns")
    table.add_column("Pattern", style="cyan")
    table.add_column("Confidence", justify="right")
    table.add_column("Evidence")
    
    for p in detected:
        confidence = f"{p.get('confidence', 0):.0%}"
        evidence = ", ".join(p.get("evidence", [])[:3])
        table.add_row(p["name"], confidence, evidence)
    
    console.print(table)
