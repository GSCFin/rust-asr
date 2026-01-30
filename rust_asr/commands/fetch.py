"""Fetch command - Clone/fetch Rust repositories from GitHub."""

import asyncio
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TaskProgressColumn

console = Console()


def execute(count: int, output: str, metadata_only: bool) -> None:
    """Fetch top Rust repositories by stars."""
    asyncio.run(_fetch_top_repos(count, output, metadata_only))


def execute_champions(repos: list[str], output: str, metadata_only: bool) -> None:
    """Fetch specific champion repositories."""
    asyncio.run(_fetch_specific_repos(repos, output, metadata_only))


async def _fetch_top_repos(count: int, output: str, metadata_only: bool) -> None:
    """Fetch top repos from GitHub API."""
    from rust_asr.repos import github, fetcher
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[cyan]Fetching top {count} Rust repositories...[/cyan]")
    
    # Get repo list from GitHub
    repos = await github.fetch_top_rust_repos(count)
    
    # Save metadata
    metadata_file = output_path / "repos_metadata.json"
    await github.save_metadata(repos, metadata_file)
    console.print(f"[green]✓[/green] Metadata saved: {metadata_file}")
    
    if metadata_only:
        return
    
    # Clone repos
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Cloning repositories...", total=len(repos))
        
        for repo in repos:
            repo_name = repo["full_name"]
            try:
                fetcher.clone_repo(repo_name, output_path)
            except Exception as e:
                console.print(f"[yellow]⚠ Failed to clone {repo_name}: {e}[/yellow]")
            progress.advance(task)
    
    console.print(f"\n[bold green]Fetched {len(repos)} repositories![/bold green]")


async def _fetch_specific_repos(repos: list[str], output: str, metadata_only: bool) -> None:
    """Fetch specific repos by name."""
    from rust_asr.repos import github, fetcher
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[cyan]Fetching {len(repos)} champion repositories...[/cyan]")
    
    # Get metadata for each repo
    repo_data = await github.fetch_repos_metadata(repos)
    
    # Save metadata
    metadata_file = output_path / "champions_metadata.json"
    await github.save_metadata(repo_data, metadata_file)
    console.print(f"[green]✓[/green] Metadata saved: {metadata_file}")
    
    if metadata_only:
        return
    
    # Clone repos
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Cloning repositories...", total=len(repos))
        
        for repo_name in repos:
            try:
                fetcher.clone_repo(repo_name, output_path)
                console.print(f"[green]✓[/green] Cloned: {repo_name}")
            except Exception as e:
                console.print(f"[yellow]⚠ Failed to clone {repo_name}: {e}[/yellow]")
            progress.advance(task)
    
    console.print(f"\n[bold green]Fetched {len(repos)} champion repositories![/bold green]")
