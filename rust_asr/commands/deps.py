"""Deps command - Generate dependency graphs."""

from pathlib import Path
from rich.console import Console

console = Console()


def execute(path: str, format: str) -> None:
    """Generate dependency graph for a project."""
    from rust_asr.analysis import dependency
    
    project_path = Path(path)
    
    console.print(f"[cyan]Analyzing dependencies: {project_path.name}[/cyan]")
    
    # Run analysis
    dep_graph = dependency.analyze(project_path)
    
    # Export in requested format
    if format == "mermaid":
        console.print(dependency.to_mermaid(dep_graph))
    elif format == "dot":
        console.print(dependency.to_dot(dep_graph))
    elif format == "json":
        import json
        console.print(json.dumps(dep_graph, indent=2))
    
    # Show stats
    nodes = dep_graph.get("nodes", [])
    edges = dep_graph.get("edges", [])
    
    console.print(f"\n[green]✓[/green] {len(nodes)} crates, {len(edges)} dependencies")
    
    # Identify core components (high in-degree)
    core = [n for n in nodes if n.get("in_degree", 0) >= 3]
    if core:
        console.print("\n[bold]Core Components (high in-degree):[/bold]")
        for c in sorted(core, key=lambda x: x.get("in_degree", 0), reverse=True)[:5]:
            console.print(f"  • {c['name']} (in-degree: {c.get('in_degree', 0)})")
