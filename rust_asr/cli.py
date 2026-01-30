"""
CLI entry point for Rust ASR toolkit.
"""

import click
from rich.console import Console
from rich.panel import Panel

from rust_asr import __version__, CHAMPION_PROJECTS

console = Console()


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """🦀 Rust ASR - Software Architecture Recovery Toolkit"""
    pass


@main.command()
@click.option("--path", "-p", type=click.Path(exists=True), help="Path to local project")
@click.option("--repo", "-r", type=str, help="GitHub repository (owner/repo format)")
@click.option("--output", "-o", type=str, default="asr-output", help="Output directory")
def analyze(path: str | None, repo: str | None, output: str) -> None:
    """Analyze a Rust project's architecture."""
    from rust_asr.commands import analyze as run_analyze
    
    if not path and not repo:
        console.print("[red]Error: Either --path or --repo must be specified[/red]")
        return
    
    run_analyze.execute(path, repo, output)


@main.command()
@click.option("--path", "-p", type=click.Path(exists=True), required=True, help="Path to project")
@click.option("--format", "-f", type=click.Choice(["mermaid", "dot", "json"]), default="mermaid")
def deps(path: str, format: str) -> None:
    """Generate dependency graph."""
    from rust_asr.commands import deps as run_deps
    
    run_deps.execute(path, format)


@main.command()
@click.option("--path", "-p", type=click.Path(exists=True), required=True, help="Path to project")
@click.option("--public-only", is_flag=True, help="Show only public API")
def modules(path: str, public_only: bool) -> None:
    """Analyze module structure and visibility."""
    from rust_asr.commands import modules as run_modules
    
    run_modules.execute(path, public_only)


@main.command()
@click.option("--count", "-n", type=int, default=100, help="Number of repos to fetch")
@click.option("--output", "-o", type=str, default="repos", help="Output directory")
@click.option("--metadata-only", is_flag=True, help="Only fetch metadata, don't clone")
@click.option("--champions", is_flag=True, help="Fetch only champion projects")
def fetch(count: int, output: str, metadata_only: bool, champions: bool) -> None:
    """Fetch top Rust repositories from GitHub."""
    from rust_asr.commands import fetch as run_fetch
    
    if champions:
        repos = [repo for repo, _ in CHAMPION_PROJECTS]
        console.print(Panel.fit(
            "\n".join([f"• {r}" for r in repos]),
            title="[bold cyan]Champion Projects[/bold cyan]"
        ))
        run_fetch.execute_champions(repos, output, metadata_only)
    else:
        run_fetch.execute(count, output, metadata_only)


@main.command()
@click.option("--path", "-p", type=click.Path(exists=True), required=True, help="Path to project")
def patterns(path: str) -> None:
    """Detect architectural patterns in a project."""
    from rust_asr.commands import patterns as run_patterns
    
    run_patterns.execute(path)


@main.command()
@click.option("--output", "-o", type=str, default="handbook", help="Output directory")
def handbook(output: str) -> None:
    """Generate the Software Architect Handbook."""
    from rust_asr.commands import handbook as run_handbook
    
    run_handbook.execute(output)


@main.command()
@click.option("--path", "-p", type=click.Path(exists=True), required=True, help="Path to project")
@click.option("--output", "-o", type=str, default="flamegraphs", help="Output directory")
def flamegraph(path: str, output: str) -> None:
    """Generate CPU flamegraph for a project."""
    from rust_asr.commands import flamegraph as run_flamegraph
    
    run_flamegraph.execute(path, output)


@main.command()
@click.option("--path", "-p", type=click.Path(exists=True), required=True, help="Path to project")
def tracing(path: str) -> None:
    """Analyze tracing/async instrumentation usage."""
    from rust_asr.commands import tracing as run_tracing
    
    run_tracing.execute(path)


@main.command("ai-analyze")
@click.option("--path", "-p", type=click.Path(exists=True), required=True, help="Path to project")
@click.option("--type", "-t", "analysis_type", 
              type=click.Choice(["summary", "c4", "patterns", "ddd"]), 
              default="summary", help="Analysis type")
@click.option("--output", "-o", type=str, help="Save output to file")
def ai_analyze(path: str, analysis_type: str, output: str | None) -> None:
    """AI-powered architecture analysis using Gemini."""
    from rust_asr.commands import ai_analyze as run_ai
    
    run_ai.execute(path, analysis_type, output)


@main.command()
@click.option("--path", "-p", type=click.Path(exists=True), required=True, help="Path to project")
@click.option("--output", "-o", type=str, default="architecture", help="Output directory")
@click.option("--format", "-f", type=click.Choice(["mermaid", "json"]), default="mermaid", help="Output format")
@click.option("--level", "-l", type=click.Choice(["context", "container", "component", "all"]), 
              default="all", help="C4 diagram level")
def architecture(path: str, output: str, format: str, level: str) -> None:
    """Extract system architecture (C4 diagrams, style detection)."""
    from rust_asr.commands import architecture as run_arch
    
    run_arch.execute(path, output, format, level)


@main.command("ai-architecture")
@click.option("--path", "-p", type=click.Path(exists=True), required=True, help="Path to project")
@click.option("--output", "-o", type=str, default="ai-architecture", help="Output directory")
@click.option("--adrs-only", is_flag=True, help="Only extract ADRs")
@click.option("--deployment-only", is_flag=True, help="Only analyze deployment model")
@click.option("--component", "-c", type=str, default=None, help="Generate AI C4 component diagram for crate")
def ai_architecture(path: str, output: str, adrs_only: bool, deployment_only: bool, component: str | None) -> None:
    """AI-enhanced architecture analysis (ADRs, refined styles, deployment)."""
    import asyncio
    from pathlib import Path
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rust_asr.ai import ai_architecture as ai_arch
    
    project_path = Path(path)
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[cyan]AI Architecture Analysis: {project_path.name}[/cyan]")
    
    async def run_analysis():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            if component:
                task = progress.add_task(f"Generating C4 component diagram for {component}...", total=None)
                diagram = await ai_arch.generate_enhanced_c4_component(project_path, component)
                progress.remove_task(task)
                out_file = output_path / f"c4_component_{component.replace('-', '_')}.md"
                out_file.write_text(f"# C4 Component Diagram: {component}\n\n{diagram}")
                console.print(f"[green]✓[/green] Component diagram saved to: {out_file}")
                return
            
            if adrs_only:
                task = progress.add_task("Extracting ADRs...", total=None)
                adrs = await ai_arch.extract_adrs(project_path)
                progress.remove_task(task)
                (output_path / "inferred_adrs.md").write_text(adrs)
                console.print(f"[green]✓[/green] ADRs saved to: {output_path / 'inferred_adrs.md'}")
                return
            
            if deployment_only:
                task = progress.add_task("Analyzing deployment model...", total=None)
                deployment = await ai_arch.analyze_deployment_model(project_path)
                progress.remove_task(task)
                (output_path / "deployment_model.md").write_text(deployment)
                console.print(f"[green]✓[/green] Deployment saved to: {output_path / 'deployment_model.md'}")
                return
            
            task = progress.add_task("Running full AI analysis...", total=None)
            results = await ai_arch.full_ai_architecture_analysis(project_path, output_path)
            progress.remove_task(task)
            
            console.print(f"[green]✓[/green] Analysis complete!")
            console.print(f"  • AI report: {output_path / 'ai_architecture_report.md'}")
            console.print(f"  • ADRs: {output_path / 'inferred_adrs.md'}")
            console.print(f"  • Deployment: {output_path / 'deployment_model.md'}")
    
    asyncio.run(run_analysis())


@main.command("compare-patterns")
@click.option("--output", "-o", type=str, default="handbook/pattern_comparison.md", help="Output path")
@click.option("--repos-dir", type=click.Path(exists=True), default="repos", help="Directory containing repos")
def compare_patterns(output: str, repos_dir: str) -> None:
    """Compare patterns across champion projects."""
    from pathlib import Path
    from rust_asr.analysis import pattern_comparison
    from rust_asr import CHAMPION_PROJECTS
    
    repos_path = Path(repos_dir)
    project_paths = []
    
    # Find champion projects
    for repo, _ in CHAMPION_PROJECTS:
        repo_name = repo.split("/")[1]
        repo_path = repos_path / repo_name
        if repo_path.exists():
            project_paths.append(repo_path)
            console.print(f"[green]✓[/green] Found: {repo_name}")
        else:
            console.print(f"[yellow]⚠[/yellow] Missing: {repo_name}")
    
    if not project_paths:
        console.print("[red]No projects found. Run 'rust-asr fetch --champions' first.[/red]")
        return
    
    console.print(f"\n[cyan]Comparing {len(project_paths)} projects...[/cyan]")
    
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pattern_comparison.generate_handbook_page(project_paths, output_path)
    
    console.print(f"[green]✓[/green] Generated: {output_path}")


@main.command()
@click.option("--path", "-p", type=click.Path(exists=True), required=True, help="Path to project")
@click.option("--output", "-o", type=str, default="project-docs", help="Output directory")
@click.option("--sections", "-s", type=str, default=None, help="Comma-separated sections (architecture,domain,api,paths,dev,llm-context)")
@click.option("--with-ai", is_flag=True, help="Include AI-enhanced analysis")
@click.option("--with-llm-context", is_flag=True, help="Generate 06-llm-context/ section with repomix export")
@click.option("--chunk-size", type=str, default="2mb", help="Chunk size for repomix split (e.g., '2mb', '500kb')")
def docs(path: str, output: str, sections: str | None, with_ai: bool, with_llm_context: bool, chunk_size: str) -> None:
    """Generate architecture documentation for a project."""
    from rust_asr.commands import docs as run_docs
    
    run_docs.execute(path, output, sections, with_ai, with_llm_context, chunk_size)


if __name__ == "__main__":
    main()
