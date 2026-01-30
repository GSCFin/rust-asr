"""Pattern Library - Cross-project pattern aggregation and documentation."""

from pathlib import Path
from typing import Any


def build_pattern_library(
    detected_patterns: list[dict[str, Any]],
    project_name: str,
) -> dict[str, Any]:
    """
    Build a pattern library from detected patterns.
    
    Organizes patterns with descriptions, code examples, and usage recommendations.
    """
    library = {
        "project": project_name,
        "patterns": [],
    }
    
    for pattern in detected_patterns:
        pattern_entry = {
            "name": pattern.get("name", "Unknown"),
            "confidence": pattern.get("confidence", 0),
            "evidence": pattern.get("evidence", []),
            "description": PATTERN_DESCRIPTIONS.get(pattern.get("name", ""), ""),
            "when_to_use": PATTERN_USAGE.get(pattern.get("name", ""), []),
            "related_patterns": PATTERN_RELATIONS.get(pattern.get("name", ""), []),
        }
        library["patterns"].append(pattern_entry)
    
    library["patterns"].sort(key=lambda x: -x["confidence"])
    
    return library


PATTERN_DESCRIPTIONS = {
    "Tower Service": """The Tower Service pattern provides a composable abstraction for request/response processing. 
Each Service takes a request and returns a future containing the response. Services can be wrapped in 
Layers to add cross-cutting concerns like timeouts, retries, and rate limiting.""",
    
    "Actor Model": """The Actor Model organizes code into independent actors that communicate only through 
asynchronous messages. Each actor has its own state and message queue, eliminating shared mutable state 
and making concurrency easier to reason about.""",
    
    "ECS (Entity-Component-System)": """ECS separates data (Components) from behavior (Systems), with Entities 
being simple identifiers. This data-oriented design provides excellent cache locality and makes it easy 
to add new behaviors without modifying existing code.""",
    
    "Type-State": """Type-State uses the type system to encode state machine transitions at compile time. 
Different states are represented as different types, making invalid state transitions impossible.""",
    
    "Builder": """The Builder pattern constructs complex objects step by step, allowing for fluent APIs 
and optional configuration. In Rust, builders often consume self to enable method chaining.""",
    
    "Error Handling (thiserror)": """thiserror provides derive macros for creating custom error types with 
Display implementations. Ideal for library code where callers need to match on specific error variants.""",
    
    "Error Handling (anyhow)": """anyhow provides flexible error handling for applications, allowing any 
error type and easy context attachment. Best for application code where error details are for users.""",
    
    "Async/Await Runtime": """Async runtimes like Tokio provide the executor and I/O primitives for 
running async Rust code. They enable efficient concurrent I/O without callback hell.""",
    
    "CRDT": """Conflict-free Replicated Data Types enable distributed systems to handle concurrent 
updates without coordination. Changes merge automatically without conflicts.""",
}

PATTERN_USAGE = {
    "Tower Service": [
        "Request/response processing pipelines",
        "HTTP middleware composition",
        "Rate limiting, retries, timeouts as composable layers",
        "gRPC service implementations",
    ],
    "Actor Model": [
        "Managing complex concurrent state",
        "Building fault-tolerant systems",
        "When you need isolation between components",
        "Web applications with per-request state",
    ],
    "ECS (Entity-Component-System)": [
        "Game development",
        "Simulations with many similar entities",
        "When you need to add behaviors dynamically",
        "Performance-critical systems with many objects",
    ],
    "Type-State": [
        "Connection lifecycle management",
        "Protocol state machines",
        "Builder patterns with required fields",
        "Preventing invalid API usage at compile time",
    ],
    "Builder": [
        "Complex object construction",
        "Optional configuration with defaults",
        "Fluent API design",
        "Test fixtures with customization",
    ],
    "Error Handling (thiserror)": [
        "Library development",
        "When callers need to handle specific errors",
        "Creating domain-specific error hierarchies",
    ],
    "Error Handling (anyhow)": [
        "Application development",
        "CLI tools",
        "When errors are primarily for logging/display",
    ],
    "Async/Await Runtime": [
        "Network I/O",
        "Web servers and clients",
        "Concurrent task processing",
        "Any I/O-bound workloads",
    ],
}

PATTERN_RELATIONS = {
    "Tower Service": ["Builder", "Async/Await Runtime"],
    "Actor Model": ["Async/Await Runtime", "Error Handling (anyhow)"],
    "Type-State": ["Builder"],
    "Builder": ["Type-State"],
    "Error Handling (thiserror)": ["Error Handling (anyhow)"],
    "Error Handling (anyhow)": ["Error Handling (thiserror)"],
    "Async/Await Runtime": ["Tower Service", "Actor Model"],
}


def export_pattern_library(library: dict[str, Any], output_path: Path) -> None:
    """Export pattern library to markdown file."""
    lines = [
        f"# Pattern Library: {library['project']}",
        "",
        "## Detected Patterns",
        "",
    ]
    
    for pattern in library["patterns"]:
        lines.append(f"### {pattern['name']}")
        lines.append(f"**Confidence:** {pattern['confidence']:.0%}")
        lines.append("")
        
        if pattern["description"]:
            lines.append("#### Description")
            lines.append(pattern["description"])
            lines.append("")
        
        if pattern["evidence"]:
            lines.append("#### Evidence")
            for ev in pattern["evidence"][:5]:
                lines.append(f"- {ev}")
            lines.append("")
        
        if pattern["when_to_use"]:
            lines.append("#### When to Use")
            for use in pattern["when_to_use"]:
                lines.append(f"- {use}")
            lines.append("")
        
        if pattern["related_patterns"]:
            lines.append("#### Related Patterns")
            lines.append(", ".join(pattern["related_patterns"]))
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    output_path.write_text("\n".join(lines))
