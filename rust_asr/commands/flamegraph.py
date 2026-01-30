"""Flamegraph command - Generate CPU flamegraphs."""

from pathlib import Path
from rich.console import Console

console = Console()


def execute(path: str, output: str) -> None:
    """Generate flamegraph for a project."""
    from rust_asr.analysis.dynamic import flamegraph
    
    project_path = Path(path)
    output_path = Path(output)
    
    console.print(f"[cyan]Generating flamegraph: {project_path.name}[/cyan]")
    
    # Check prerequisites
    prereqs = flamegraph.check_prerequisites()
    console.print("\n[bold]Prerequisites:[/bold]")
    for tool, available in prereqs.items():
        status = "✅" if available else "❌"
        console.print(f"  {status} {tool}")
    
    if not prereqs.get("cargo-flamegraph"):
        console.print("\n[yellow]Install with: cargo install flamegraph[/yellow]")
        return
    
    # Generate
    result = flamegraph.generate(project_path, output_path)
    
    if result["success"]:
        console.print(f"\n[green]✓[/green] Flamegraph saved: {result['svg_path']}")
        
        # Analyze hotspots
        hotspots = flamegraph.analyze_hotspots(Path(result["svg_path"]))
        if hotspots:
            console.print("\n[bold]Top Hot Functions:[/bold]")
            for h in hotspots[:10]:
                console.print(f"  • {h['function'][:60]}")
    else:
        console.print(f"\n[red]✗[/red] Error: {result['error']}")
