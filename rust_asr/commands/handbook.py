"""Handbook command - Generate Software Architect Handbook."""

from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def execute(output: str, repos_dir: str = "repos") -> None:
    """Generate the Software Architect Handbook."""
    from rust_asr import CHAMPION_PROJECTS
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    repos_path = Path(repos_dir)
    
    console.print("[cyan]Generating Software Architect Handbook...[/cyan]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Part I: Foundation
        task = progress.add_task("Writing Part I: Foundation...", total=None)
        _write_part1(output_path)
        progress.remove_task(task)
        
        # Part II: Patterns
        task = progress.add_task("Writing Part II: Patterns...", total=None)
        _write_part2(output_path)
        progress.remove_task(task)
        
        # Part III: Techniques
        task = progress.add_task("Writing Part III: Techniques...", total=None)
        _write_part3(output_path)
        progress.remove_task(task)
        
        # Part IV: Case Studies
        task = progress.add_task("Writing Part IV: Case Studies...", total=None)
        _write_part4(output_path, CHAMPION_PROJECTS, repos_path)
        progress.remove_task(task)
        
        # Part V: System Architecture
        task = progress.add_task("Writing Part V: System Architecture...", total=None)
        _write_part5(output_path)
        progress.remove_task(task)
        
        # Part VI: Pattern Comparison
        task = progress.add_task("Writing Part VI: Pattern Comparison...", total=None)
        _write_part6(output_path, CHAMPION_PROJECTS, repos_path)
        progress.remove_task(task)
    
    console.print(f"\n[bold green]Handbook generated![/bold green] Location: {output_path}")


def _write_part1(output_path: Path) -> None:
    """Write Part I: Foundation - The Rustacean Architect Mindset."""
    content = """# Part I: Foundation - The Rustacean Architect Mindset

## Chapter 1: How Ownership Defines Architecture

Rust's ownership system isn't just a memory safety feature - it's an architectural constraint.

### The Core Principle

In Rust, **data flows through ownership boundaries**. This means:

- Components can't freely share mutable state
- Message passing becomes natural
- Boundaries are explicit and compiler-enforced

### Implications for Design

1. **Components must declare their data ownership**
2. **Shared state requires explicit synchronization**
3. **Lifetime annotations reveal data dependencies**

## Chapter 2: Shared Mutable State is the Enemy

Traditional architectures often rely on shared mutable state.
In Rust, this requires fighting the compiler. Instead:

- Use message passing (channels)
- Use immutable shared state (`Arc<T>`)  
- Use interior mutability carefully (`Mutex<T>`, `RwLock<T>`)

## Chapter 3: Design by Borrow Checking

Let the borrow checker guide your architecture:

```rust
// The compiler tells you when components are too coupled
fn process(data: &mut Data, other: &mut Data) {
    // If these are the same, compiler rejects
}
```
"""
    (output_path / "part1_foundation.md").write_text(content)


def _write_part2(output_path: Path) -> None:
    """Write Part II: Design Patterns."""
    content = """# Part II: Design Patterns

## Tower Service Pattern

The foundation of Rust web services. A `Service` transforms requests into responses:

```rust
pub trait Service<Request> {
    type Response;
    type Error;
    type Future: Future<Output = Result<Self::Response, Self::Error>>;
    
    fn call(&self, req: Request) -> Self::Future;
}
```

**Layer composition** creates the "onion" architecture:
- Timeout layer (outer)
- Retry layer
- Auth layer  
- Business logic (inner)

## Error Handling: Library vs Application

### Library Pattern (thiserror)

```rust
#[derive(thiserror::Error, Debug)]
pub enum MyError {
    #[error("network timeout")]
    Timeout,
    #[error("invalid credentials")]
    InvalidCredentials,
}
```

### Application Pattern (anyhow)

```rust
fn main() -> anyhow::Result<()> {
    let result = do_something()
        .context("failed to do something")?;
    Ok(())
}
```

## Type-State Pattern

Encode state machines in the type system:

```rust
struct Connection<State> { ... }

impl Connection<Disconnected> {
    fn connect(self) -> Connection<Connected> { ... }
}

impl Connection<Connected> {
    fn send(&self, data: &[u8]) { ... }
}
```
"""
    (output_path / "part2_patterns.md").write_text(content)


def _write_part3(output_path: Path) -> None:
    """Write Part III: Recovery Techniques."""
    content = """# Part III: Architecture Recovery Techniques

## Static Analysis Pipeline

1. **Dependency Graph Mining**
   - Use `cargo depgraph` to visualize crate dependencies
   - Calculate in-degree/out-degree for core component detection
   - High in-degree = Core/Utility component
   - High out-degree = Interface layer (CLI, API)

2. **Module Structure Analysis**
   - Use `cargo modules structure`
   - Map `pub` vs `pub(crate)` boundaries
   - `pub(crate)` = Implementation detail
   - `pub` across crates = Shared component

3. **Call Hierarchy**
   - Use rust-analyzer LSP
   - Bottom-up: Find core algorithms, trace callers
   - Identify use cases

## Dynamic Analysis

1. **Tracing**
   - Use `tokio-tracing` for async systems
   - Understand Future lifecycle

2. **Flamegraphs**
   - Identify hot paths
   - Find performance bottlenecks

## AI-Assisted Analysis

Use LLMs to:
- Generate C4 diagrams from code structure
- Identify bounded contexts (DDD)
- Summarize architectural decisions
"""
    (output_path / "part3_techniques.md").write_text(content)


def _write_part4(output_path: Path, champions: list[tuple[str, str]], repos_path: Path) -> None:
    """Write Part IV: Case Studies with auto-analysis."""
    from rust_asr.analysis import architecture, patterns
    
    content = """# Part IV: Case Studies

"""
    for repo, category in champions:
        name = repo.split("/")[1]
        repo_path = repos_path / name
        
        content += f"""## {name} ({category})

### Architecture Overview

"""
        if repo_path.exists():
            # Run auto-analysis
            styles = architecture.detect_architecture_style(repo_path)
            workspace = architecture.analyze_workspace(repo_path)
            detected_patterns = patterns.analyze(repo_path)
            
            if workspace.get("is_workspace"):
                content += f"**Workspace:** {workspace.get('package_count', 0)} crates\n\n"
            
            if styles:
                content += "**Architecture Styles:**\n"
                for s in styles[:3]:
                    content += f"- {s['style']} ({s['confidence']:.0%})\n"
                content += "\n"
        else:
            content += f"*Analysis pending - run `rust-asr analyze --repo {repo}`*\n\n"

        content += """### Key Patterns

"""
        if repo_path.exists() and detected_patterns:
            for p in detected_patterns[:5]:
                content += f"- **{p['name']}** ({p['confidence']:.0%})\n"
            content += "\n"
        else:
            content += "*To be extracted*\n\n"

        content += """### Lessons Learned

*See detailed case study in `case_studies/` directory*

---

"""
    
    (output_path / "part4_case_studies.md").write_text(content)


def _write_part5(output_path: Path) -> None:
    """Write Part V: System Architecture."""
    content = """# Part V: System Architecture Patterns in Rust

## Common Architectural Styles

### Multi-Crate Workspace

Most large Rust projects use a workspace structure:

```toml
[workspace]
members = [
    "crates/core",
    "crates/api",
    "crates/cli",
]
```

**Benefits:**
- Clear separation of concerns
- Parallel compilation
- Independent versioning

### Hexagonal/Ports-Adapters

Rust traits naturally support this pattern:

```rust
trait UserRepository {
    fn find_by_id(&self, id: UserId) -> Option<User>;
}

struct PostgresUserRepo { ... }
struct InMemoryUserRepo { ... }

impl UserRepository for PostgresUserRepo { ... }
impl UserRepository for InMemoryUserRepo { ... }
```

### Plugin Architecture

Common in extensible systems like Bevy:

```rust
trait Plugin {
    fn build(&self, app: &mut App);
}

app.add_plugins(DefaultPlugins)
   .add_plugins(MyPlugin);
```

## C4 Model for Rust

### Context Level
- System and its external dependencies
- Users and external systems

### Container Level  
- Individual crates within a workspace
- Main binaries and libraries

### Component Level
- Modules within a crate
- Key traits and structs

### Code Level
- Function implementations
- Data structures

## Communication Patterns

| Pattern | Crate | Use Case |
|---------|-------|----------|
| Tokio Channels | `tokio::sync` | Async message passing |
| Crossbeam | `crossbeam-channel` | High-performance channels |
| Shared State | `Arc<Mutex<T>>` | Mutable shared data |
| Actor Model | `actix`, `xactor` | Complex concurrent systems |
"""
    (output_path / "part5_system_architecture.md").write_text(content)


def _write_part6(output_path: Path, champions: list[tuple[str, str]], repos_path: Path) -> None:
    """Write Part VI: Pattern Comparison Matrix."""
    from rust_asr.analysis import pattern_comparison

    project_paths = []
    for repo, _ in champions:
        name = repo.split("/")[1]
        repo_path = repos_path / name
        if repo_path.exists():
            project_paths.append(repo_path)
    
    if project_paths:
        comparison = pattern_comparison.compare_patterns(project_paths)
        content = pattern_comparison.generate_comparison_matrix(comparison)
    else:
        content = """# Part VI: Pattern Comparison Matrix

*No champion projects found. Run `rust-asr fetch --champions` first.*
"""
    
    (output_path / "part6_pattern_comparison.md").write_text(content)

