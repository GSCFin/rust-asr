"""LLM Questions Bank - Deep analysis prompts and questions."""

from pathlib import Path
from typing import Any


DEEP_ANALYSIS_QUESTIONS = {
    "architecture": {
        "title": "Architecture Analysis",
        "questions": [
            "What is the primary architectural style used in this codebase? What evidence supports this conclusion?",
            "How is the codebase organized? Describe the layering or modularization approach.",
            "Are there any layer violations or architectural anti-patterns?",
            "What are the key abstractions in this system and why were they chosen?",
            "How does the error handling strategy support the overall architecture?",
        ],
    },
    "data_flow": {
        "title": "Data Flow Analysis",
        "questions": [
            "Trace the data flow from input to output for the main use case.",
            "Where are the primary data transformations happening?",
            "How is state managed throughout the application?",
            "Are there any bottlenecks in the data pipeline?",
            "How does data move between different layers/modules?",
        ],
    },
    "patterns": {
        "title": "Design Patterns",
        "questions": [
            "Which design patterns are used in this codebase? Are they implemented correctly?",
            "What Rust-specific idioms are leveraged (Type-State, Builder, NewType, etc.)?",
            "Are there any anti-patterns that should be refactored?",
            "How does the codebase leverage Rust's ownership system for safety?",
            "What traits are used to abstract behavior and why?",
        ],
    },
    "concurrency": {
        "title": "Concurrency & Async",
        "questions": [
            "How is concurrency handled in this codebase?",
            "What async runtime is used and how is it configured?",
            "Are there any potential race conditions or deadlocks?",
            "How is shared state managed between concurrent tasks?",
            "What synchronization primitives are used (Mutex, RwLock, channels)?",
        ],
    },
    "contributor_onboarding": {
        "title": "Contributor Onboarding",
        "questions": [
            "Where should a new contributor start to understand this codebase?",
            "What are the key files to read first?",
            "What conventions does this project follow?",
            "How should I set up my development environment?",
            "What is the testing strategy and how do I run tests?",
        ],
    },
    "extending": {
        "title": "Extension & Modification",
        "questions": [
            "How would I add a new feature to this system?",
            "What extension points exist in the architecture?",
            "How should new modules integrate with existing code?",
            "What patterns should I follow for consistency?",
            "Are there any areas that need refactoring before extending?",
        ],
    },
}


PROMPT_TEMPLATES = {
    "architecture_review": """You are a senior Rust software architect reviewing a codebase.

Based on the provided code and knowledge graph, perform a comprehensive architecture review:

1. **Architecture Style**: Identify the primary architectural style (Hexagonal, Layered, ECS, Actor, etc.)
2. **Component Analysis**: List the major components and their responsibilities
3. **Dependency Analysis**: Evaluate the dependency structure for coupling issues
4. **Recommendations**: Provide 3-5 actionable improvements

Focus on Rust-specific patterns and idioms. Be specific with file/module references.
""",

    "code_review": """You are a Rust expert performing a code review.

Review the provided code for:
1. **Correctness**: Are there any bugs or logic errors?
2. **Safety**: Are there any unsafe patterns that could be avoided?
3. **Performance**: Are there any obvious performance issues?
4. **Idioms**: Is the code idiomatic Rust?
5. **Documentation**: Is the code well-documented?

Provide specific line references and concrete suggestions.
""",

    "refactoring_plan": """You are a senior developer planning a refactoring effort.

Based on the provided codebase analysis:
1. Identify the top 3 areas that would benefit most from refactoring
2. For each area, describe:
   - Current problems
   - Proposed solution
   - Expected benefits
   - Estimated effort
3. Prioritize the refactoring tasks

Consider maintainability, testability, and future extensibility.
""",

    "security_audit": """You are a security engineer auditing a Rust codebase.

Analyze the provided code for security concerns:
1. **Input Validation**: Are all inputs properly validated?
2. **Authentication/Authorization**: If applicable, are they implemented correctly?
3. **Unsafe Code**: Are there any unsafe blocks? Are they necessary and correct?
4. **Dependencies**: Are there any known vulnerable dependencies?
5. **Data Handling**: Is sensitive data handled appropriately?

Report findings with severity levels (Critical, High, Medium, Low).
""",

    "onboarding_guide": """You are creating an onboarding guide for new contributors.

Based on the codebase, create a guide that covers:
1. **Project Overview**: What does this project do?
2. **Architecture Summary**: High-level structure explanation
3. **Key Concepts**: Important abstractions and patterns used
4. **Getting Started**: First files/modules to explore
5. **Common Tasks**: How to add features, fix bugs, run tests

Keep the language beginner-friendly but technically accurate.
""",
}


def export_questions_bank(output_path: Path) -> None:
    """Export the questions bank to a markdown file."""
    lines = [
        "# LLM Analysis Questions Bank",
        "",
        "Use these questions to guide deep analysis of the codebase with an LLM.",
        "",
    ]
    
    for category_key, category in DEEP_ANALYSIS_QUESTIONS.items():
        lines.append(f"## {category['title']}")
        lines.append("")
        for i, question in enumerate(category["questions"], 1):
            lines.append(f"{i}. {question}")
        lines.append("")
    
    output_path.write_text("\n".join(lines))


def export_prompt_templates(output_path: Path) -> None:
    """Export prompt templates to a markdown file."""
    lines = [
        "# LLM Prompt Templates",
        "",
        "Ready-to-use prompts for deep codebase analysis.",
        "",
    ]
    
    for name, template in PROMPT_TEMPLATES.items():
        title = name.replace("_", " ").title()
        lines.append(f"## {title}")
        lines.append("")
        lines.append("```")
        lines.append(template.strip())
        lines.append("```")
        lines.append("")
    
    output_path.write_text("\n".join(lines))


def get_contextual_questions(
    patterns: list[str],
    has_async: bool = False,
    has_unsafe: bool = False,
) -> list[str]:
    """Generate context-aware questions based on detected patterns."""
    questions = []
    
    questions.extend(DEEP_ANALYSIS_QUESTIONS["architecture"]["questions"][:2])
    questions.extend(DEEP_ANALYSIS_QUESTIONS["patterns"]["questions"][:2])
    
    if has_async:
        questions.extend(DEEP_ANALYSIS_QUESTIONS["concurrency"]["questions"][:2])
    
    if "Tower Service" in patterns:
        questions.append("How is the Tower middleware stack organized? What layers are applied?")
    
    if "Actor Model" in patterns:
        questions.append("How do actors communicate? What message types are defined?")
    
    if "ECS (Entity-Component-System)" in patterns:
        questions.append("What are the main systems and what components do they operate on?")
    
    if has_unsafe:
        questions.append("What unsafe code exists and is it properly encapsulated?")
    
    return questions
