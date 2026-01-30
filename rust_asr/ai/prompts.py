"""Prompt templates for AI-assisted architecture analysis."""


C4_CONTEXT_PROMPT = """You are a software architect analyzing a Rust codebase.

Based on the following codebase structure, generate a C4 Context diagram in Mermaid format.

{codebase_context}

Generate:
1. System Context diagram showing external actors and systems
2. Brief description of the system's purpose

Output format:
```mermaid
C4Context
    title System Context diagram for {project_name}
    
    Person(user, "User", "Description")
    System(system, "{project_name}", "Description")
    System_Ext(ext, "External System", "Description")
    
    Rel(user, system, "Uses")
```
"""


C4_CONTAINER_PROMPT = """You are a software architect analyzing a Rust codebase.

Based on the following codebase structure, generate a C4 Container diagram in Mermaid format.

{codebase_context}

The workspace contains these crates:
{crate_list}

Generate a C4 Container diagram showing:
- Main containers (binaries, libraries)
- Data stores if any
- External dependencies

Output format:
```mermaid
C4Container
    title Container diagram for {project_name}
    
    Container(api, "API", "Rust", "Description")
    ContainerDb(db, "Database", "Type", "Description")
    
    Rel(api, db, "Reads/writes")
```
"""


DDD_BOUNDED_CONTEXT_PROMPT = """You are a domain-driven design expert analyzing a Rust codebase.

Based on the following codebase structure and modules, identify Bounded Contexts.

{codebase_context}

Module structure:
{module_tree}

For each identified Bounded Context, describe:
1. Name
2. Core domain concepts
3. Key aggregates/entities
4. Integration points with other contexts

Output as a structured list.
"""


PATTERN_ANALYSIS_PROMPT = """You are a Rust architecture expert. Analyze the following code for architectural patterns.

{codebase_context}

Detected patterns from static analysis:
{static_patterns}

For each pattern:
1. Confirm if the pattern is correctly identified
2. Explain how it's implemented
3. Identify any variations from the standard pattern
4. Suggest improvements if any

Focus on Rust-specific patterns like Tower Service, Type-State, Builder, etc.
"""


ARCHITECTURE_SUMMARY_PROMPT = """You are a senior software architect creating documentation.

Based on the following analysis of a Rust project:

Codebase:
{codebase_context}

Dependencies:
{dependency_graph}

Detected Patterns:
{patterns}

Metrics:
{metrics}

Write a concise architecture summary including:
1. System Overview (2-3 sentences)
2. Key Architectural Decisions
3. Main Components and their responsibilities
4. Notable patterns and their purpose
5. Potential improvements

Keep the summary under 500 words.
"""


# New AI-enhanced architecture prompts

ARCHITECTURE_STYLE_REFINEMENT_PROMPT = """You are a Rust software architect. Given the following project analysis, provide a refined assessment of the architecture style.

Project: {project_name}

Workspace structure:
{workspace_info}

Detected styles from static analysis:
{detected_styles}

Communication patterns:
{communication_patterns}

Key dependencies:
{dependencies}

Tasks:
1. Validate or refine the detected architecture styles
2. Identify the PRIMARY architecture style (pick only one)
3. Explain WHY this style was chosen with 2-3 concrete evidence points
4. List any SECONDARY styles that complement the primary

Output format (JSON):
```json
{{
    "primary_style": "Style Name",
    "primary_confidence": 85,
    "primary_evidence": ["Evidence 1", "Evidence 2"],
    "secondary_styles": [
        {{"name": "Style", "confidence": 60, "reason": "..."}}
    ],
    "architectural_summary": "2-3 sentence summary"
}}
```
"""


ADR_EXTRACTION_PROMPT = """You are an experienced Rust architect. Analyze this codebase and infer Architectural Decision Records (ADRs) from the code patterns.

Project: {project_name}

Codebase context:
{codebase_context}

Detected patterns:
{patterns}

For each inferred ADR, provide:
1. Title (concise decision statement)
2. Status: Accepted
3. Context: What problem does this solve?
4. Decision: What was decided?
5. Consequences: Trade-offs and implications
6. Evidence: Code patterns that reveal this decision

Generate 3-5 most significant ADRs.

Output format:
## ADR-001: [Title]

**Status**: Accepted  
**Context**: [Problem description]  
**Decision**: [What was chosen]  
**Consequences**: 
- Positive: [benefit]
- Negative: [trade-off]

**Evidence**: [Code patterns showing this decision]

---
"""


C4_COMPONENT_ENHANCED_PROMPT = """You are a Rust software architect. Generate a detailed C4 Component diagram for this crate.

Crate: {crate_name}
Project: {project_name}

Module structure:
{module_structure}

Public API (exports):
{public_api}

Key types:
{key_types}

Generate a C4 Component diagram showing:
- Key components (modules) within the crate
- Relationships between components
- External interfaces

Output as a Mermaid diagram with explanatory comments:
```mermaid
C4Component
title Component diagram for {crate_name}

Container_Boundary({crate_name}_boundary, "{crate_name}") {{
    Component(mod1, "module1", "Purpose")
    Component(mod2, "module2", "Purpose")
}}

Rel(mod1, mod2, "Uses")
```
"""


DEPLOYMENT_MODEL_PROMPT = """You are a DevOps-aware Rust architect. Analyze this project and describe its deployment model.

Project: {project_name}

Cargo.toml features:
{features}

Binary targets:
{binaries}

Dependencies suggesting deployment:
{deployment_deps}

Infer and describe:
1. Deployment model (standalone binary, library, service, CLI tool, etc.)
2. Runtime requirements
3. Configuration approach
4. Scaling characteristics

Output as structured markdown.
"""


def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with provided values."""
    return template.format(**kwargs)

