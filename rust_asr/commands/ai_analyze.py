"""AI-analyze command - LLM-powered architecture analysis."""

import asyncio
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def execute(path: str, analysis_type: str, output: str | None) -> None:
    """Run AI-powered architecture analysis."""
    asyncio.run(_analyze_async(path, analysis_type, output))


async def _analyze_async(path: str, analysis_type: str, output: str | None) -> None:
    """Async implementation of AI analysis."""
    from rust_asr.ai import mapper, llm
    
    project_path = Path(path)
    
    console.print(f"[cyan]AI Analysis: {project_path.name}[/cyan]")
    console.print(f"[dim]Analysis type: {analysis_type}[/dim]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Map codebase
        task = progress.add_task("Mapping codebase...", total=None)
        context = mapper.map_codebase(project_path)
        progress.remove_task(task)
        console.print(f"[green]✓[/green] Codebase mapped ({len(context)} chars)")
        
        # Run AI analysis
        task = progress.add_task("Running AI analysis...", total=None)
        try:
            result = await llm.analyze_architecture(context, analysis_type)
            progress.remove_task(task)
            console.print(f"[green]✓[/green] Analysis complete")
        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]✗[/red] AI error: {e}")
            return
    
    # Display result
    console.print("\n")
    console.print(Markdown(result))
    
    # Save if output specified
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result)
        console.print(f"\n[green]✓[/green] Saved to: {output_path}")
