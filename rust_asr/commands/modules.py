"""Modules command - Analyze module structure."""

from pathlib import Path
from rich.console import Console
from rich.tree import Tree

console = Console()


def execute(path: str, public_only: bool) -> None:
    """Analyze module structure and visibility."""
    from rust_asr.analysis import modules
    
    project_path = Path(path)
    
    console.print(f"[cyan]Analyzing modules: {project_path.name}[/cyan]")
    
    # Run analysis
    mod_tree = modules.analyze(project_path, public_only=public_only)
    
    # Display tree
    tree = Tree(f"[bold]{project_path.name}[/bold]")
    _build_tree(tree, mod_tree)
    console.print(tree)
    
    # Stats
    total = _count_modules(mod_tree)
    pub_count = _count_public(mod_tree)
    
    console.print(f"\n[green]✓[/green] {total} modules ({pub_count} public)")


def _build_tree(tree: Tree, node: dict) -> None:
    """Recursively build Rich tree from module tree."""
    for child in node.get("children", []):
        visibility = child.get("visibility", "")
        name = child.get("name", "unknown")
        
        if visibility == "pub":
            label = f"[green]{name}[/green] (pub)"
        elif visibility == "pub(crate)":
            label = f"[yellow]{name}[/yellow] (pub(crate))"
        else:
            label = f"[dim]{name}[/dim]"
        
        branch = tree.add(label)
        _build_tree(branch, child)


def _count_modules(node: dict) -> int:
    """Count total modules."""
    count = 1
    for child in node.get("children", []):
        count += _count_modules(child)
    return count


def _count_public(node: dict) -> int:
    """Count public modules."""
    count = 1 if node.get("visibility") == "pub" else 0
    for child in node.get("children", []):
        count += _count_public(child)
    return count
