"""Tracing command - Analyze async/tracing usage."""

from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()


def execute(path: str) -> None:
    """Analyze tracing usage in a project."""
    from rust_asr.analysis.dynamic import tracing
    
    project_path = Path(path)
    
    console.print(f"[cyan]Analyzing tracing: {project_path.name}[/cyan]")
    
    # Detect tracing usage
    info = tracing.detect_tracing_usage(project_path)
    
    # Display results
    console.print("\n[bold]Tracing Configuration:[/bold]")
    console.print(f"  Uses tracing:      {'✅' if info['uses_tracing'] else '❌'}")
    console.print(f"  Uses tokio:        {'✅' if info['uses_tokio_tracing'] else '❌'}")
    console.print(f"  Instrumented fns:  {info.get('instrumented_count', 0)}")
    
    if info["instrumented_functions"]:
        console.print("\n[bold]Instrumented Functions:[/bold]")
        table = Table()
        table.add_column("Function")
        table.add_column("File")
        
        for f in info["instrumented_functions"][:15]:
            table.add_row(f["function"], f["file"][:40])
        
        console.print(table)
    
    if info["span_patterns"]:
        console.print(f"\n[bold]Event Levels:[/bold] {', '.join(info['span_patterns'])}")
