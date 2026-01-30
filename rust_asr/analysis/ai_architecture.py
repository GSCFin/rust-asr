"""AI-enhanced architecture analysis for Rust projects.

Uses LLM to validate and refine static analysis results:
- Confirm detected architectural patterns
- Suggest missed patterns
- Provide architecture style confidence scores
"""

from pathlib import Path
from typing import Any


def create_validation_prompt(analysis_results: dict[str, Any]) -> str:
    """
    Create a prompt for LLM to validate architecture analysis.
    
    Args:
        analysis_results: Results from static analysis modules
        
    Returns:
        Formatted prompt string for LLM
    """
    styles = analysis_results.get("architecture_styles", [])
    patterns = analysis_results.get("patterns", [])
    workspace = analysis_results.get("workspace", {})
    
    prompt = f"""You are a Rust software architecture expert. Analyze the following static analysis results and validate/refine the detected architectural patterns.

## Project: {analysis_results.get('project_name', 'Unknown')}

## Workspace Info
- Package count: {workspace.get('package_count', 'N/A')}
- Is workspace: {workspace.get('is_workspace', False)}

## Detected Architecture Styles
"""
    
    for style in styles[:5]:
        prompt += f"- **{style['style']}** ({style['confidence']:.0%}): {', '.join(style.get('evidence', []))}\n"
    
    prompt += "\n## Detected Design Patterns\n"
    
    for pattern in patterns[:5]:
        prompt += f"- **{pattern['name']}** ({pattern['confidence']:.0%}): {', '.join(pattern.get('evidence', []))}\n"
    
    prompt += """

## Your Task

Based on the detected patterns and your expertise in Rust architecture, please:

1. **Validate**: Are the detected patterns accurate? What's your confidence level?
2. **Refine**: Suggest any corrections or nuances to the detection
3. **Missed Patterns**: What important patterns might be missing from detection?
4. **Architecture Classification**: What's the primary architecture archetype?

Options for archetype:
- Reactor/Proactor (async runtime like Tokio)
- Actor-based (Actix, xactor)
- ECS (Bevy, specs)
- Plugin Architecture (extensible core)
- Hexagonal/Clean Architecture (ports & adapters)
- Layered Monolith
- Microservices (multi-binary workspace)

Respond in JSON format:
```json
{
  "validated_patterns": [{"name": "...", "confidence": 0.9, "notes": "..."}],
  "corrections": ["..."],
  "missed_patterns": ["..."],
  "primary_archetype": "...",
  "secondary_archetypes": ["..."],
  "overall_assessment": "..."
}
```
"""
    return prompt


def create_c4_enhancement_prompt(
    c4_container: str, 
    knowledge_graph: dict[str, Any]
) -> str:
    """
    Create a prompt for LLM to enhance C4 container diagram.
    
    Args:
        c4_container: Current Mermaid C4 container diagram
        knowledge_graph: Knowledge graph with nodes and edges
        
    Returns:
        Formatted prompt string for LLM
    """
    prompt = f"""You are a software architect specializing in C4 diagrams. Review and enhance this C4 Container diagram for a Rust project.

## Current Diagram
```mermaid
{c4_container}
```

## Knowledge Graph Summary
- Total entities: {knowledge_graph.get('stats', {}).get('total_nodes', 0)}
- Total relationships: {knowledge_graph.get('stats', {}).get('total_edges', 0)}
- Clusters: {knowledge_graph.get('stats', {}).get('total_clusters', 0)}

## Top Relationships
"""
    
    edges = knowledge_graph.get("edges", [])
    rel_counts: dict[str, int] = {}
    for edge in edges:
        rel = edge.get("relationship", "unknown")
        rel_counts[rel] = rel_counts.get(rel, 0) + 1
    
    for rel, count in sorted(rel_counts.items(), key=lambda x: -x[1])[:5]:
        prompt += f"- {rel}: {count}\n"
    
    prompt += """

## Your Task

Enhance the C4 diagram by:
1. Adding missing important containers
2. Improving relationship labels (uses, extends, implements)
3. Categorizing containers (Core, Interface, Infrastructure)
4. Adding notes for key design decisions

Return enhanced Mermaid C4 diagram only, no explanation needed.
"""
    return prompt


def create_adr_extraction_prompt(readme_content: str, cargo_toml: str) -> str:
    """
    Create a prompt to extract Architecture Decision Records from docs.
    
    Args:
        readme_content: Content of README.md
        cargo_toml: Content of Cargo.toml
        
    Returns:
        Formatted prompt string for LLM
    """
    prompt = f"""You are extracting Architecture Decision Records (ADRs) from a Rust project.

## README.md
{readme_content[:3000]}

## Cargo.toml
{cargo_toml[:1000]}

## Your Task

Extract implicit ADRs from the documentation. Look for:
- Why certain dependencies were chosen
- Architecture style decisions
- Performance trade-offs
- Error handling strategy
- Concurrency model choices

Format each ADR as:
```
### ADR-001: [Title]
**Status**: Accepted
**Context**: [Why this decision was needed]
**Decision**: [What was decided]
**Consequences**: [Impact of the decision]
```

Extract 3-5 key ADRs.
"""
    return prompt


def fuse_static_and_ai_results(
    static_results: dict[str, Any],
    ai_response: dict[str, Any],
) -> dict[str, Any]:
    """
    Fuse static analysis results with AI validation.
    
    Args:
        static_results: Results from static analysis
        ai_response: Parsed response from LLM
        
    Returns:
        Combined results with adjusted confidence scores
    """
    fused = static_results.copy()
    
    if "validated_patterns" in ai_response:
        validated = {p["name"]: p for p in ai_response["validated_patterns"]}
        
        for pattern in fused.get("patterns", []):
            if pattern["name"] in validated:
                ai_pattern = validated[pattern["name"]]
                original_conf = pattern["confidence"]
                ai_conf = ai_pattern.get("confidence", original_conf)
                pattern["confidence"] = (original_conf + ai_conf) / 2
                pattern["ai_validated"] = True
                pattern["ai_notes"] = ai_pattern.get("notes", "")
    
    if "corrections" in ai_response:
        fused["ai_corrections"] = ai_response["corrections"]
    
    if "missed_patterns" in ai_response:
        fused["ai_suggested_patterns"] = ai_response["missed_patterns"]
    
    if "primary_archetype" in ai_response:
        fused["primary_archetype"] = ai_response["primary_archetype"]
        fused["secondary_archetypes"] = ai_response.get("secondary_archetypes", [])
    
    fused["ai_assessment"] = ai_response.get("overall_assessment", "")
    
    return fused


def export_ai_analysis_report(
    fused_results: dict[str, Any], 
    output_path: Path
) -> None:
    """Export AI-enhanced analysis as markdown report."""
    lines = [
        f"# AI-Enhanced Architecture Analysis: {fused_results.get('project_name', 'Unknown')}",
        "",
        "## Primary Architecture Archetype",
        "",
        f"**{fused_results.get('primary_archetype', 'Not determined')}**",
        "",
    ]
    
    secondary = fused_results.get("secondary_archetypes", [])
    if secondary:
        lines.append("Secondary patterns: " + ", ".join(secondary))
        lines.append("")
    
    lines.extend(["## Validated Patterns", ""])
    
    for pattern in fused_results.get("patterns", []):
        if pattern.get("ai_validated"):
            lines.append(f"### {pattern['name']} ({pattern['confidence']:.0%})")
            if pattern.get("ai_notes"):
                lines.append(f"> {pattern['ai_notes']}")
            lines.append("")
    
    corrections = fused_results.get("ai_corrections", [])
    if corrections:
        lines.extend(["## AI Corrections", ""])
        for c in corrections:
            lines.append(f"- {c}")
        lines.append("")
    
    suggested = fused_results.get("ai_suggested_patterns", [])
    if suggested:
        lines.extend(["## Suggested Additional Patterns", ""])
        for s in suggested:
            lines.append(f"- {s}")
        lines.append("")
    
    assessment = fused_results.get("ai_assessment", "")
    if assessment:
        lines.extend(["## Overall Assessment", "", assessment, ""])
    
    output_path.write_text("\n".join(lines))
