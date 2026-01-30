"""CLI command for generating architecture documentation."""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from rust_asr.export import architecture as arch_export
from rust_asr.export import executive_summary as exec_export
from rust_asr.export import domain_model as domain_export
from rust_asr.export import api_interfaces as api_export
from rust_asr.export import critical_paths as paths_export
from rust_asr.export import development_guide as dev_export
from rust_asr.export import llm_context as llm_export
from rust_asr.export import semantic_index as semantic_export
from rust_asr.export import pattern_library as pattern_export
from rust_asr.export import llm_questions as questions_export
from rust_asr.analysis import architecture, patterns as pattern_analyzer
from rust_asr.analysis import knowledge_graph


console = Console()


def execute(
    path: str,
    output: str,
    sections: str | None = None,
    with_ai: bool = False,
    with_llm_context: bool = False,
    chunk_size: str = "2mb",
) -> None:
    """Execute architecture documentation export.
    
    Args:
        path: Path to Rust project
        output: Output directory for docs
        sections: Comma-separated sections (architecture,domain,api,paths,dev,summary,llm-context)
        with_ai: Include AI-enhanced analysis
        with_llm_context: Generate LLM context section (06-llm-context/)
        chunk_size: Chunk size for repomix split (e.g., "2mb", "500kb")
    """
    project_path = Path(path)
    output_path = Path(output)
    
    console.print(Panel.fit(
        f"[bold cyan]Generating Documentation:[/bold cyan] {project_path.name}",
        title="📄 Architecture Docs Export"
    ))
    
    # Determine which sections to generate
    all_sections = {"summary", "architecture", "domain", "api", "paths", "dev", "llm-context"}
    if sections:
        requested = {s.strip().lower() for s in sections.split(",")}
        active_sections = requested & all_sections
    else:
        active_sections = all_sections - {"llm-context"}  # llm-context requires explicit flag
    
    # Add llm-context if explicitly requested
    if with_llm_context:
        active_sections.add("llm-context")
    
    console.print(f"[dim]Sections: {', '.join(sorted(active_sections))}[/dim]")
    
    # Run comprehensive analysis once
    console.print("\n[dim]Running analysis...[/dim]")
    analysis = architecture.analyze(project_path, include_dynamic=True)
    analysis["patterns"] = pattern_analyzer.analyze(project_path)
    console.print("[green]✓[/green] Analysis complete")
    
    # AI-enhanced ADRs
    ai_adrs = None
    if with_ai:
        console.print("[dim]Running AI-enhanced analysis...[/dim]")
        try:
            from rust_asr.ai import ai_architecture
            import asyncio
            
            async def get_adrs():
                return await ai_architecture.extract_adrs(project_path)
            
            ai_adrs = asyncio.run(get_adrs())
            console.print("[green]✓[/green] AI analysis complete")
        except Exception as e:
            console.print(f"[yellow]![/yellow] AI analysis failed: {e}")
    
    all_files: dict[str, Path] = {}
    
    # Generate 01-architecture section
    if "architecture" in active_sections:
        console.print("\n[bold]Generating 01-architecture/[/bold]")
        files = arch_export.export_architecture_docs(
            project_path,
            output_path,
            ai_adrs=ai_adrs,
            include_patterns=True,
            include_tracing=True,
        )
        all_files.update({f"01-architecture/{k}": v for k, v in files.items()})
    
    # Generate 02-domain-model section
    if "domain" in active_sections:
        console.print("[bold]Generating 02-domain-model/[/bold]")
        files = domain_export.export_domain_model(project_path, output_path, analysis)
        all_files.update({f"02-domain-model/{k}": v for k, v in files.items()})
    
    # Generate 03-api-interfaces section
    if "api" in active_sections:
        console.print("[bold]Generating 03-api-interfaces/[/bold]")
        files = api_export.export_api_interfaces(project_path, output_path, analysis)
        all_files.update({f"03-api-interfaces/{k}": v for k, v in files.items()})
    
    # Generate 04-critical-paths section
    if "paths" in active_sections:
        console.print("[bold]Generating 04-critical-paths/[/bold]")
        files = paths_export.export_critical_paths(project_path, output_path, analysis)
        all_files.update({f"04-critical-paths/{k}": v for k, v in files.items()})
    
    # Generate 05-development-guide section
    if "dev" in active_sections:
        console.print("[bold]Generating 05-development-guide/[/bold]")
        files = dev_export.export_development_guide(project_path, output_path, analysis)
        all_files.update({f"05-development-guide/{k}": v for k, v in files.items()})
    
    # Generate 06-llm-context section
    if "llm-context" in active_sections:
        console.print("[bold]Generating 06-llm-context/[/bold]")
        llm_context_path = output_path / "06-llm-context"
        llm_context_path.mkdir(parents=True, exist_ok=True)
        
        # 1. Full codebase dump with repomix
        console.print("  [dim]Exporting codebase with repomix...[/dim]")
        context_result = llm_export.export_full_context(
            project_path, llm_context_path, chunk_size=chunk_size
        )
        for f in context_result.get("files_created", []):
            fname = Path(f).name
            all_files[f"06-llm-context/{fname}"] = Path(f)
        console.print(f"  [green]✓[/green] {context_result['file_count']} file(s), {context_result['method']}")
        
        # 2. Knowledge graph
        console.print("  [dim]Building knowledge graph...[/dim]")
        graph = knowledge_graph.build_knowledge_graph(project_path)
        knowledge_graph.export_knowledge_graph(graph, llm_context_path / "semantic-map.json")
        knowledge_graph.export_knowledge_graph_summary(graph, llm_context_path / "knowledge-graph-summary.md")
        all_files["06-llm-context/semantic-map.json"] = llm_context_path / "semantic-map.json"
        all_files["06-llm-context/knowledge-graph-summary.md"] = llm_context_path / "knowledge-graph-summary.md"
        console.print(f"  [green]✓[/green] {graph['stats']['total_nodes']} nodes, {graph['stats']['total_edges']} edges")
        
        # 3. Semantic index
        console.print("  [dim]Building semantic index...[/dim]")
        index = semantic_export.build_semantic_index(project_path, graph)
        semantic_export.export_semantic_index_markdown(index, llm_context_path / "navigation-guide.md")
        all_files["06-llm-context/navigation-guide.md"] = llm_context_path / "navigation-guide.md"
        console.print("  [green]✓[/green] Semantic index complete")
        
        # 4. Pattern library
        console.print("  [dim]Building pattern library...[/dim]")
        patterns = analysis.get("patterns", [])
        library = pattern_export.build_pattern_library(patterns, project_path.name)
        pattern_export.export_pattern_library(library, llm_context_path / "pattern-library.md")
        all_files["06-llm-context/pattern-library.md"] = llm_context_path / "pattern-library.md"
        console.print(f"  [green]✓[/green] {len(patterns)} patterns documented")
        
        # 5. Questions bank & prompt templates
        console.print("  [dim]Exporting prompts & questions...[/dim]")
        questions_export.export_questions_bank(llm_context_path / "questions-bank.md")
        questions_export.export_prompt_templates(llm_context_path / "prompt-templates.md")
        all_files["06-llm-context/questions-bank.md"] = llm_context_path / "questions-bank.md"
        all_files["06-llm-context/prompt-templates.md"] = llm_context_path / "prompt-templates.md"
        console.print("  [green]✓[/green] Prompts exported")
    
    # Generate 00-executive-summary (last, as it references other sections)
    if "summary" in active_sections:
        console.print("[bold]Generating 00-executive-summary.md[/bold]")
        summary_path = exec_export.export_executive_summary(project_path, output_path, analysis)
        all_files["00-executive-summary.md"] = summary_path
    
    # Display results
    table = Table(title="Generated Files")
    table.add_column("Section", style="cyan")
    table.add_column("Path")
    
    for name in sorted(all_files.keys()):
        table.add_row(name, str(all_files[name]))
    
    console.print(table)
    console.print(f"\n[green]✓[/green] Documentation saved to: {output_path}")
