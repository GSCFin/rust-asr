"""AI-enhanced architecture analysis using Gemini."""

import asyncio
import json
import re
from pathlib import Path
from typing import Any

from rust_asr.ai import llm, mapper, prompts
from rust_asr.analysis import architecture


async def refine_architecture_style(
    project_path: Path,
    static_analysis: dict[str, Any],
) -> dict[str, Any]:
    """Use AI to refine and validate detected architecture styles.
    
    Args:
        project_path: Path to the Rust project
        static_analysis: Results from static architecture analysis
        
    Returns:
        Refined architecture assessment with AI insights
    """
    client = llm.get_client()
    
    # Prepare context
    workspace_info = json.dumps(static_analysis.get("workspace", {}), indent=2)
    detected_styles = "\n".join(
        f"- {s.get('style', 'Unknown')} ({s.get('confidence', 0):.0%}): {s.get('description', '')}"
        for s in static_analysis.get("styles", [])
    )
    comm_patterns = "\n".join(
        f"- {p.get('pattern', 'Unknown')}: {p.get('usage_count', 0)} usages"
        for p in static_analysis.get("communication_patterns", [])
    )
    
    # Get key dependencies from packages
    deps = []
    for pkg in static_analysis.get("workspace", {}).get("packages", []):
        deps.extend(pkg.get("dependencies", []))
    deps_str = ", ".join(set(deps[:20]))
    
    prompt = prompts.ARCHITECTURE_STYLE_REFINEMENT_PROMPT.format(
        project_name=project_path.name,
        workspace_info=workspace_info,
        detected_styles=detected_styles,
        communication_patterns=comm_patterns,
        dependencies=deps_str,
    )
    
    system_prompt = (
        "You are a senior Rust software architect. "
        "Provide accurate, evidence-based assessments. "
        "Output valid JSON only when requested."
    )
    
    result = await client.generate(prompt, system_prompt, temperature=0.3)
    
    # Parse JSON from response
    try:
        json_match = re.search(r'```json\s*(.*?)\s*```', result, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
    except (json.JSONDecodeError, AttributeError):
        pass
    
    return {"raw_response": result, "parse_error": True}


async def extract_adrs(
    project_path: Path,
    patterns: list[dict[str, Any]] | None = None,
) -> str:
    """Use AI to infer ADRs from code patterns.
    
    Args:
        project_path: Path to the Rust project
        patterns: Optional pre-detected patterns
        
    Returns:
        Markdown-formatted ADRs
    """
    client = llm.get_client()
    
    # Map codebase
    context = mapper.map_codebase(project_path, max_tokens=50000)
    
    # Format patterns
    patterns_str = ""
    if patterns:
        patterns_str = "\n".join(
            f"- {p['pattern']} ({p['confidence']}%)"
            for p in patterns
        )
    else:
        patterns_str = "No pre-detected patterns provided."
    
    prompt = prompts.ADR_EXTRACTION_PROMPT.format(
        project_name=project_path.name,
        codebase_context=context,
        patterns=patterns_str,
    )
    
    system_prompt = (
        "You are an experienced Rust software architect who documents architectural decisions. "
        "Generate well-structured ADRs based on observable code patterns."
    )
    
    return await client.generate(prompt, system_prompt, temperature=0.5, max_tokens=4096)


async def generate_enhanced_c4_component(
    project_path: Path,
    crate_name: str,
) -> str:
    """Generate AI-enhanced C4 Component diagram for a specific crate.
    
    Args:
        project_path: Path to the Rust project
        crate_name: Name of the crate to analyze
        
    Returns:
        Mermaid diagram string
    """
    client = llm.get_client()
    
    # Find crate path
    crate_path = None
    for potential in [
        project_path / crate_name,
        project_path / "crates" / crate_name,
        project_path / crate_name.replace("-", "_"),
    ]:
        if (potential / "Cargo.toml").exists():
            crate_path = potential
            break
    
    if not crate_path:
        crate_path = project_path
    
    # Get module structure
    src_path = crate_path / "src"
    module_structure = ""
    if src_path.exists():
        modules = []
        for rs_file in sorted(src_path.rglob("*.rs")):
            rel = rs_file.relative_to(crate_path)
            modules.append(f"- {rel}")
        module_structure = "\n".join(modules[:50])
    
    # Get key types
    key_types = mapper.extract_key_types(crate_path)
    types_str = "\n".join(
        f"- {t['kind']}: {t['name']} ({t['file']})"
        for t in key_types[:30]
    )
    
    # Read lib.rs for public API
    public_api = ""
    lib_rs = src_path / "lib.rs"
    if lib_rs.exists():
        try:
            content = lib_rs.read_text()
            # Extract pub use and pub mod lines
            pub_lines = [
                line.strip() for line in content.split("\n")
                if line.strip().startswith(("pub use", "pub mod"))
            ]
            public_api = "\n".join(pub_lines[:20])
        except Exception:
            pass
    
    prompt = prompts.C4_COMPONENT_ENHANCED_PROMPT.format(
        project_name=project_path.name,
        crate_name=crate_name,
        module_structure=module_structure or "No modules found",
        public_api=public_api or "No public API exports found",
        key_types=types_str or "No key types found",
    )
    
    system_prompt = (
        "You are a Rust software architect creating C4 diagrams. "
        "Generate valid Mermaid C4 diagrams. Be concise but informative."
    )
    
    return await client.generate(prompt, system_prompt, temperature=0.3)


async def analyze_deployment_model(
    project_path: Path,
) -> str:
    """Analyze and infer the project's deployment model.
    
    Args:
        project_path: Path to the Rust project
        
    Returns:
        Markdown description of deployment model
    """
    client = llm.get_client()
    
    # Get workspace info
    workspace = architecture.analyze_workspace(project_path)
    
    # Extract features from Cargo.toml
    features = []
    binaries = []
    deployment_deps = []
    
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text()
            # Simple feature extraction
            if "[features]" in content:
                feature_section = content.split("[features]")[1].split("\n[")[0]
                for line in feature_section.split("\n"):
                    if "=" in line:
                        features.append(line.split("=")[0].strip())
            
            # Binary targets
            if "[[bin]]" in content:
                for match in re.finditer(r'name\s*=\s*"([^"]+)"', content):
                    binaries.append(match.group(1))
        except Exception:
            pass
    
    # Check for deployment-related deps
    deployment_keywords = [
        "tokio", "axum", "actix", "rocket", "warp",  # web
        "clap", "structopt",  # CLI
        "diesel", "sqlx", "sea-orm",  # database
        "redis", "kafka", "rabbitmq",  # messaging
        "k8s", "docker",  # container
    ]
    
    for pkg in workspace.get("packages", []):
        for dep in pkg.get("dependencies", []):
            # Dependencies are stored as strings
            dep_name = dep.lower() if isinstance(dep, str) else dep.get("name", "").lower()
            if any(kw in dep_name for kw in deployment_keywords):
                deployment_deps.append(dep_name)
    
    prompt = prompts.DEPLOYMENT_MODEL_PROMPT.format(
        project_name=project_path.name,
        features=", ".join(features[:20]) or "None detected",
        binaries=", ".join(binaries) or "Library only",
        deployment_deps=", ".join(list(set(deployment_deps))[:15]) or "None detected",
    )
    
    system_prompt = (
        "You are a DevOps-aware Rust architect. "
        "Describe deployment models based on evidence from the codebase."
    )
    
    return await client.generate(prompt, system_prompt, temperature=0.4)


async def full_ai_architecture_analysis(
    project_path: Path,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Run full AI-enhanced architecture analysis.
    
    Args:
        project_path: Path to the Rust project
        output_dir: Optional directory to save results
        
    Returns:
        Complete analysis results
    """
    project_path = Path(project_path)
    
    # Run static analysis first
    workspace = architecture.analyze_workspace(project_path)
    styles = architecture.detect_architecture_style(project_path)
    comm_patterns = architecture.detect_communication_patterns(project_path)
    
    static_analysis = {
        "workspace": workspace,
        "styles": styles,
        "communication_patterns": comm_patterns,
    }
    
    # Run AI enhancements in parallel
    refined_style, adrs, deployment = await asyncio.gather(
        refine_architecture_style(project_path, static_analysis),
        extract_adrs(project_path),
        analyze_deployment_model(project_path),
    )
    
    results = {
        "project_name": project_path.name,
        "static_analysis": static_analysis,
        "ai_refined_style": refined_style,
        "inferred_adrs": adrs,
        "deployment_model": deployment,
    }
    
    # Save if output directory specified
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON summary
        (output_dir / "ai_analysis.json").write_text(
            json.dumps(results, indent=2, default=str)
        )
        
        # Save ADRs
        (output_dir / "inferred_adrs.md").write_text(adrs)
        
        # Save deployment model
        (output_dir / "deployment_model.md").write_text(deployment)
        
        # Generate full report
        report = _generate_report(results)
        (output_dir / "ai_architecture_report.md").write_text(report)
    
    return results


def _generate_report(results: dict[str, Any]) -> str:
    """Generate markdown report from analysis results."""
    lines = [
        f"# AI Architecture Analysis: {results['project_name']}",
        "",
        "## Architecture Style Assessment",
        "",
    ]
    
    refined = results.get("ai_refined_style", {})
    if not refined.get("parse_error"):
        lines.extend([
            f"**Primary Style**: {refined.get('primary_style', 'Unknown')} "
            f"({refined.get('primary_confidence', 0)}% confidence)",
            "",
            "### Evidence",
            "",
        ])
        for evidence in refined.get("primary_evidence", []):
            lines.append(f"- {evidence}")
        
        lines.extend(["", "### Secondary Styles", ""])
        for style in refined.get("secondary_styles", []):
            lines.append(f"- **{style.get('name')}** ({style.get('confidence')}%): {style.get('reason', '')}")
        
        lines.extend([
            "",
            "### Summary",
            "",
            refined.get("architectural_summary", ""),
            "",
        ])
    
    lines.extend([
        "---",
        "",
        "## Inferred ADRs",
        "",
        results.get("inferred_adrs", "No ADRs generated."),
        "",
        "---",
        "",
        "## Deployment Model",
        "",
        results.get("deployment_model", "No deployment model generated."),
    ])
    
    return "\n".join(lines)


def run_analysis(project_path: str, output_dir: str | None = None) -> dict[str, Any]:
    """Synchronous wrapper for full AI analysis."""
    return asyncio.run(
        full_ai_architecture_analysis(Path(project_path), Path(output_dir) if output_dir else None)
    )
