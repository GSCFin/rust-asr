"""CLI command for architecture analysis."""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

from rust_asr.analysis import architecture

console = Console()


def execute(path: str, output: str, format: str, level: str) -> None:
    """Execute architecture analysis."""
    project_path = Path(path)
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    console.print(Panel.fit(
        f"[bold cyan]Analyzing Architecture:[/bold cyan] {project_path.name}",
        title="🏗️ Architecture Analysis"
    ))
    
    # Run full analysis
    console.print("[dim]Analyzing workspace structure...[/dim]")
    analysis = architecture.analyze(project_path)
    
    # Display workspace info
    ws = analysis.get("workspace", {})
    if ws.get("is_workspace"):
        console.print(f"\n[green]✓[/green] Multi-crate workspace with {ws['package_count']} packages")
        
        table = Table(title="Workspace Packages")
        table.add_column("Name", style="cyan")
        table.add_column("Version")
        table.add_column("Dependencies")
        table.add_column("Features")
        
        for pkg in ws.get("packages", [])[:10]:
            table.add_row(
                pkg["name"],
                pkg["version"],
                str(len(pkg.get("dependencies", []))),
                ", ".join(pkg.get("features", [])[:3]) or "-"
            )
        console.print(table)
    else:
        console.print("\n[yellow]![/yellow] Single-crate project")
    
    # Display detected styles
    styles = analysis.get("architecture_styles", [])
    if styles:
        console.print("\n[bold]Detected Architecture Styles:[/bold]")
        for style in styles:
            confidence = style["confidence"]
            color = "green" if confidence > 0.7 else "yellow" if confidence > 0.4 else "dim"
            console.print(f"  [{color}]●[/{color}] {style['style']} ({confidence:.0%})")
            console.print(f"    [dim]{style['description']}[/dim]")
    
    # Display communication patterns
    patterns = analysis.get("communication_patterns", [])
    if patterns:
        console.print("\n[bold]Communication Patterns:[/bold]")
        for p in patterns[:5]:
            console.print(f"  • {p['pattern']} ({p['usage_count']} usages)")
    
    # Generate diagrams based on level
    if level in ["context", "all"]:
        console.print("\n[dim]Generating C4 Context diagram...[/dim]")
        context_diagram = architecture.generate_c4_context(project_path)
        
        if format == "mermaid":
            diagram_file = output_path / "c4_context.md"
            diagram_file.write_text(f"# C4 Context Diagram\n\n{context_diagram}")
            console.print(f"[green]✓[/green] Saved: {diagram_file}")
        
        console.print(Syntax(context_diagram, "markdown", theme="monokai", line_numbers=False))
    
    if level in ["container", "all"]:
        console.print("\n[dim]Generating C4 Container diagram...[/dim]")
        container_diagram = architecture.generate_c4_container(project_path)
        
        if format == "mermaid":
            diagram_file = output_path / "c4_container.md"
            diagram_file.write_text(f"# C4 Container Diagram\n\n{container_diagram}")
            console.print(f"[green]✓[/green] Saved: {diagram_file}")
        
        console.print(Syntax(container_diagram, "markdown", theme="monokai", line_numbers=False))
    
    if level in ["component", "all"]:
        console.print("\n[dim]Generating C4 Component diagram...[/dim]")
        component_diagram = architecture.generate_c4_component(project_path)
        
        if format == "mermaid":
            diagram_file = output_path / "c4_component.md"
            diagram_file.write_text(f"# C4 Component Diagram\n\n{component_diagram}")
            console.print(f"[green]✓[/green] Saved: {diagram_file}")
        
        console.print(Syntax(component_diagram, "markdown", theme="monokai", line_numbers=False))
    
    # Export full report
    report_file = output_path / "architecture_report.md"
    architecture.export_report(analysis, report_file, project_path.name)
    console.print(f"\n[green]✓[/green] Full report saved: {report_file}")
    
    # JSON export
    if format == "json":
        import json
        json_file = output_path / "architecture.json"
        json_file.write_text(json.dumps(analysis, indent=2, default=str))
        console.print(f"[green]✓[/green] JSON data saved: {json_file}")
