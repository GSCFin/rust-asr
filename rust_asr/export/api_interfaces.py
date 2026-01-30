"""API Interfaces documentation export module.

Generates 03-api-interfaces/ documentation:
- public-apis.md: Entry points and public traits
- internal-contracts.md: Module boundaries
- integration-points.md: External systems
"""

from pathlib import Path
from typing import Any
import re


def analyze_public_api(project_path: Path) -> dict[str, Any]:
    """Analyze public API surface from Rust source files.
    
    Extracts:
    - Public functions with signatures
    - Public structs/enums
    - Public traits with methods
    - lib.rs/main.rs exports
    """
    api_info = {
        "functions": [],
        "traits": [],
        "modules": [],
        "entry_points": [],
    }
    
    src_path = project_path / "src"
    if not src_path.exists():
        src_path = project_path
    
    fn_pattern = re.compile(r"pub\s+(?:async\s+)?fn\s+(\w+)\s*<?\s*[^>]*>?\s*\(([^)]*)\)(?:\s*->\s*([^\{;]+))?", re.MULTILINE)
    trait_fn_pattern = re.compile(r"fn\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*([^\{;]+))?", re.MULTILINE)
    mod_pattern = re.compile(r"pub\s+mod\s+(\w+)", re.MULTILINE)
    
    for rs_file in src_path.rglob("*.rs"):
        try:
            content = rs_file.read_text(errors="ignore")
            rel_path = rs_file.relative_to(project_path)
            file_name = rs_file.name
            
            for match in fn_pattern.finditer(content):
                name = match.group(1)
                params = match.group(2).strip()
                return_type = match.group(3).strip() if match.group(3) else "()"
                
                if name.startswith("_"):
                    continue
                
                param_count = params.count(",") + (1 if params and params != "&self" and params != "&mut self" else 0)
                
                api_info["functions"].append({
                    "name": name,
                    "params": param_count,
                    "return_type": return_type[:30],
                    "file": str(rel_path),
                    "is_entry": file_name in ("main.rs", "lib.rs"),
                })
            
            for match in mod_pattern.finditer(content):
                mod_name = match.group(1)
                api_info["modules"].append({
                    "name": mod_name,
                    "file": str(rel_path),
                })
                
        except Exception:
            continue
    
    # Identify entry points
    api_info["entry_points"] = [f for f in api_info["functions"] if f["is_entry"]]
    
    return api_info


def generate_public_apis(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate public-apis.md with entry points and public functions."""
    project_name = project_path.name
    api_info = analyze_public_api(project_path)
    
    lines = [
        f"# Public APIs: {project_name}",
        "",
        "## Entry Points",
        "",
    ]
    
    entry_points = api_info["entry_points"]
    if entry_points:
        lines.extend([
            "| Function | Parameters | Returns | File |",
            "|----------|------------|---------|------|",
        ])
        for fn in entry_points[:10]:
            lines.append(f"| `{fn['name']}` | {fn['params']} | `{fn['return_type']}` | {fn['file']} |")
    else:
        lines.append("*No public entry points detected in lib.rs/main.rs*")
    
    lines.extend([
        "",
        "## Public Functions",
        "",
        "| Function | Parameters | Returns | File |",
        "|----------|------------|---------|------|",
    ])
    
    non_entry = [f for f in api_info["functions"] if not f["is_entry"]]
    for fn in non_entry[:20]:
        lines.append(f"| `{fn['name']}` | {fn['params']} | `{fn['return_type']}` | {fn['file']} |")
    
    if not non_entry:
        lines.append("| *No additional public functions* | - | - | - |")
    
    return "\n".join(lines)


def generate_internal_contracts(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate internal-contracts.md with module boundaries."""
    project_name = project_path.name
    api_info = analyze_public_api(project_path)
    workspace = analysis.get("workspace", {})
    packages = workspace.get("packages", [])
    
    lines = [
        f"# Internal Contracts: {project_name}",
        "",
        "## Module Structure",
        "",
        "```mermaid",
        "graph TD",
    ]
    
    modules = api_info["modules"]
    module_names = set()
    for mod in modules[:15]:
        name = mod["name"]
        safe_name = name.replace("-", "_")
        module_names.add(safe_name)
        lines.append(f"    {safe_name}[{name}]")
    
    if not modules:
        lines.append("    main[Main Module]")
    
    lines.extend([
        "```",
        "",
        "## Module Exports",
        "",
        "| Module | Source File |",
        "|--------|-------------|",
    ])
    
    for mod in modules[:20]:
        lines.append(f"| `{mod['name']}` | {mod['file']} |")
    
    if not modules:
        lines.append("| *No public modules* | - |")
    
    # Crate boundaries
    if len(packages) > 1:
        lines.extend([
            "",
            "## Crate Boundaries",
            "",
            "| Crate | Public Items | Dependencies |",
            "|-------|--------------|--------------|",
        ])
        
        for pkg in packages[:15]:
            name = pkg.get("name", "")
            dep_count = len(pkg.get("dependencies", []))
            lines.append(f"| `{name}` | - | {dep_count} |")
    
    return "\n".join(lines)


def generate_integration_points(project_path: Path, analysis: dict[str, Any]) -> str:
    """Generate integration-points.md with external systems."""
    project_name = project_path.name
    workspace = analysis.get("workspace", {})
    packages = workspace.get("packages", [])
    
    # Categories of external dependencies
    integration_categories = {
        "HTTP/Web": ["hyper", "reqwest", "axum", "actix-web", "warp", "tower"],
        "Database": ["sqlx", "diesel", "sea-orm", "mongodb", "redis"],
        "Async Runtime": ["tokio", "async-std", "smol"],
        "Serialization": ["serde", "serde_json", "serde_yaml", "toml"],
        "CLI": ["clap", "structopt", "argh"],
        "Logging": ["tracing", "log", "env_logger", "tracing-subscriber"],
        "Testing": ["criterion", "proptest", "quickcheck", "mockall"],
    }
    
    found_integrations: dict[str, list[str]] = {}
    
    for pkg in packages:
        for dep in pkg.get("dependencies", []):
            dep_name = dep if isinstance(dep, str) else dep.get("name", "")
            for category, deps in integration_categories.items():
                if dep_name in deps:
                    if category not in found_integrations:
                        found_integrations[category] = []
                    if dep_name not in found_integrations[category]:
                        found_integrations[category].append(dep_name)
    
    lines = [
        f"# Integration Points: {project_name}",
        "",
        "## External Systems",
        "",
    ]
    
    if found_integrations:
        lines.extend([
            "| Category | Dependencies |",
            "|----------|--------------|",
        ])
        
        for category, deps in found_integrations.items():
            deps_str = ", ".join(f"`{d}`" for d in deps)
            lines.append(f"| {category} | {deps_str} |")
    else:
        lines.append("*No major external integrations detected*")
    
    # Integration diagram
    lines.extend([
        "",
        "## Integration Architecture",
        "",
        "```mermaid",
        "graph LR",
        f"    A[{project_name}]",
    ])
    
    for category, deps in list(found_integrations.items())[:5]:
        safe_cat = category.replace("/", "_").replace(" ", "_")
        lines.append(f"    A --> {safe_cat}[{category}]")
    
    if not found_integrations:
        lines.append("    A --> StdLib[Standard Library]")
    
    lines.append("```")
    
    return "\n".join(lines)


def export_api_interfaces(
    project_path: Path,
    output_dir: Path,
    analysis: dict[str, Any],
) -> dict[str, Path]:
    """Export 03-api-interfaces/ documentation.
    
    Args:
        project_path: Path to Rust project
        output_dir: Output directory
        analysis: Complete analysis data
        
    Returns:
        Dict mapping file names to paths
    """
    api_dir = Path(output_dir) / "03-api-interfaces"
    api_dir.mkdir(parents=True, exist_ok=True)
    
    files = {}
    
    # public-apis.md
    content = generate_public_apis(project_path, analysis)
    path = api_dir / "public-apis.md"
    path.write_text(content)
    files["public-apis.md"] = path
    
    # internal-contracts.md
    content = generate_internal_contracts(project_path, analysis)
    path = api_dir / "internal-contracts.md"
    path.write_text(content)
    files["internal-contracts.md"] = path
    
    # integration-points.md
    content = generate_integration_points(project_path, analysis)
    path = api_dir / "integration-points.md"
    path.write_text(content)
    files["integration-points.md"] = path
    
    return files
