"""Development Guide documentation export module.

Generates 05-development-guide/ documentation:
- getting-started.md: Setup, build, run
- code-conventions.md: Patterns, naming
- testing-strategy.md: Test structure
- contribution-guide.md: PR process
"""

from pathlib import Path
from typing import Any
import re


def analyze_testing(project_path: Path) -> dict[str, Any]:
    """Analyze testing patterns in Rust source files."""
    test_info = {
        "test_modules": 0,
        "test_functions": 0,
        "uses_criterion": False,
        "uses_proptest": False,
        "uses_mockall": False,
        "test_files": [],
        "integration_tests": [],
    }
    
    src_path = project_path / "src"
    tests_path = project_path / "tests"
    
    test_mod_pattern = re.compile(r"#\[cfg\(test\)\]", re.MULTILINE)
    test_fn_pattern = re.compile(r"#\[test\]", re.MULTILINE)
    
    # Check src for unit tests
    if src_path.exists():
        for rs_file in src_path.rglob("*.rs"):
            try:
                content = rs_file.read_text(errors="ignore")
                
                if test_mod_pattern.search(content):
                    test_info["test_modules"] += 1
                
                test_info["test_functions"] += len(test_fn_pattern.findall(content))
                
                if "criterion" in content:
                    test_info["uses_criterion"] = True
                if "proptest" in content:
                    test_info["uses_proptest"] = True
                if "mockall" in content:
                    test_info["uses_mockall"] = True
                    
            except Exception:
                continue
    
    # Check tests directory for integration tests
    if tests_path.exists():
        for rs_file in tests_path.rglob("*.rs"):
            rel_path = rs_file.relative_to(project_path)
            test_info["integration_tests"].append(str(rel_path))
    
    return test_info


def generate_getting_started(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate getting-started.md with setup instructions."""
    project_name = project_path.name
    workspace = analysis.get("workspace", {})
    packages = workspace.get("packages", [])
    
    # Detect binary targets
    has_binary = False
    binary_name = project_name
    for pkg in packages:
        if pkg.get("name") == project_name:
            has_binary = True
            break
    
    lines = [
        f"# Getting Started: {project_name}",
        "",
        "## Prerequisites",
        "",
        "- Rust 1.70+ (with `cargo`)",
        "- Git",
        "",
        "## Quick Start",
        "",
        "```bash",
        "# Clone the repository",
        f"git clone https://github.com/YOUR_ORG/{project_name}.git",
        f"cd {project_name}",
        "",
        "# Build",
        "cargo build --release",
        "",
        "# Run tests",
        "cargo test",
        "```",
        "",
        "## Building",
        "",
        "### Debug Build",
        "",
        "```bash",
        "cargo build",
        "```",
        "",
        "### Release Build",
        "",
        "```bash",
        "cargo build --release",
        "```",
        "",
    ]
    
    if has_binary:
        lines.extend([
            "## Running",
            "",
            "```bash",
            f"cargo run --release -- --help",
            "```",
            "",
        ])
    
    # Feature flags
    lines.extend([
        "## Feature Flags",
        "",
        "```bash",
        "# Build with all features",
        "cargo build --all-features",
        "",
        "# Build with specific feature",
        "cargo build --features feature_name",
        "```",
    ])
    
    return "\n".join(lines)


def generate_code_conventions(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate code-conventions.md with patterns and naming."""
    project_name = project_path.name
    patterns = analysis.get("patterns", [])
    styles = analysis.get("architecture_styles", [])
    
    lines = [
        f"# Code Conventions: {project_name}",
        "",
        "## Rust Style",
        "",
        "This project follows standard Rust conventions:",
        "",
        "- **Naming**: `snake_case` for functions/variables, `CamelCase` for types",
        "- **Formatting**: `cargo fmt` (rustfmt default)",
        "- **Linting**: `cargo clippy` with default configuration",
        "",
        "## Pre-Commit Checks",
        "",
        "```bash",
        "cargo fmt --check",
        "cargo clippy -- -D warnings",
        "cargo test",
        "```",
        "",
    ]
    
    # Detected patterns
    if patterns:
        lines.extend([
            "## Design Patterns Used",
            "",
        ])
        for pattern in patterns[:5]:
            conf = f"{pattern['confidence']:.0%}"
            lines.append(f"- **{pattern['name']}** ({conf})")
        lines.append("")
    
    # Architecture style
    if styles:
        lines.extend([
            "## Architecture Guidelines",
            "",
        ])
        for style in styles[:2]:
            lines.append(f"- **{style['style']}**: {style['description']}")
        lines.append("")
    
    lines.extend([
        "## Error Handling",
        "",
        "- Use `Result<T, E>` for fallible operations",
        "- Prefer `?` operator over `.unwrap()`",
        "- Use `anyhow` for application errors",
        "- Use `thiserror` for library error types",
    ])
    
    return "\n".join(lines)


def generate_testing_strategy(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate testing-strategy.md with test structure."""
    project_name = project_path.name
    test_info = analyze_testing(project_path)
    
    lines = [
        f"# Testing Strategy: {project_name}",
        "",
        "## Test Summary",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Test modules (`#[cfg(test)]`) | {test_info['test_modules']} |",
        f"| Test functions (`#[test]`) | {test_info['test_functions']} |",
        f"| Integration test files | {len(test_info['integration_tests'])} |",
        "",
        "## Test Tooling",
        "",
        f"- Criterion benchmarks: {'✅' if test_info['uses_criterion'] else '❌'}",
        f"- Property testing (proptest): {'✅' if test_info['uses_proptest'] else '❌'}",
        f"- Mocking (mockall): {'✅' if test_info['uses_mockall'] else '❌'}",
        "",
        "## Running Tests",
        "",
        "```bash",
        "# All tests",
        "cargo test",
        "",
        "# Specific test",
        "cargo test test_name",
        "",
        "# With output",
        "cargo test -- --nocapture",
        "",
        "# Integration tests only",
        "cargo test --test '*'",
        "```",
    ]
    
    if test_info["integration_tests"]:
        lines.extend([
            "",
            "## Integration Tests",
            "",
        ])
        for test_file in test_info["integration_tests"][:10]:
            lines.append(f"- `{test_file}`")
    
    return "\n".join(lines)


def generate_contribution_guide(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate contribution-guide.md with PR process."""
    project_name = project_path.name
    
    lines = [
        f"# Contributing to {project_name}",
        "",
        "## Development Workflow",
        "",
        "1. Fork the repository",
        "2. Create a feature branch: `git checkout -b feature/my-feature`",
        "3. Make changes and commit: `git commit -m 'Add feature'`",
        "4. Push to your fork: `git push origin feature/my-feature`",
        "5. Open a Pull Request",
        "",
        "## Before Submitting",
        "",
        "```bash",
        "# Format code",
        "cargo fmt",
        "",
        "# Run linter",
        "cargo clippy -- -D warnings",
        "",
        "# Run tests",
        "cargo test",
        "```",
        "",
        "## Commit Message Format",
        "",
        "Use conventional commits:",
        "",
        "- `feat:` New feature",
        "- `fix:` Bug fix",
        "- `docs:` Documentation only",
        "- `refactor:` Code change without new feature or fix",
        "- `test:` Adding tests",
        "",
        "## Code Review Process",
        "",
        "1. All PRs require at least one approval",
        "2. CI must pass (fmt, clippy, tests)",
        "3. Maintain test coverage",
    ]
    
    return "\n".join(lines)


def export_development_guide(
    project_path: Path,
    output_dir: Path,
    analysis: dict[str, Any],
) -> dict[str, Path]:
    """Export 05-development-guide/ documentation.
    
    Args:
        project_path: Path to Rust project
        output_dir: Output directory
        analysis: Complete analysis data
        
    Returns:
        Dict mapping file names to paths
    """
    guide_dir = Path(output_dir) / "05-development-guide"
    guide_dir.mkdir(parents=True, exist_ok=True)
    
    files = {}
    
    # getting-started.md
    content = generate_getting_started(project_path, analysis)
    path = guide_dir / "getting-started.md"
    path.write_text(content)
    files["getting-started.md"] = path
    
    # code-conventions.md
    content = generate_code_conventions(project_path, analysis)
    path = guide_dir / "code-conventions.md"
    path.write_text(content)
    files["code-conventions.md"] = path
    
    # testing-strategy.md
    content = generate_testing_strategy(project_path, analysis)
    path = guide_dir / "testing-strategy.md"
    path.write_text(content)
    files["testing-strategy.md"] = path
    
    # contribution-guide.md
    content = generate_contribution_guide(project_path, analysis)
    path = guide_dir / "contribution-guide.md"
    path.write_text(content)
    files["contribution-guide.md"] = path
    
    return files
