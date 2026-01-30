"""Architectural pattern detection."""

import re
from pathlib import Path
from typing import Any

from .architecture import _iter_source_files


# Pattern signatures to look for - improved to reduce false positives
PATTERN_SIGNATURES = {
    "Tower Service": {
        "keywords": ["ServiceBuilder", "tower::"],
        "imports": ["tower", "tower_http", "tower_service"],
        "traits": ["Service<Request>", "tower::Service"],
    },
    "Actor Model": {
        "keywords": ["Addr<", "Handler<", "Recipient<"],
        "imports": ["actix", "actix_web", "xactor", "ractor"],
        "traits": [],  # Removed generic keywords that cause false positives
    },
    "ECS (Entity-Component-System)": {
        "keywords": ["Query<", "Commands", "Res<", "ResMut<"],
        "imports": ["bevy_ecs", "specs", "legion", "hecs"],
        "traits": [],  # Removed generic keywords that cause false positives
    },
    "Type-State": {
        "patterns": [
            r"struct\s+\w+<\w+>",  # Generic struct
            r"impl\s+\w+<\w+>",     # Impl with type parameter as state
            r"fn\s+\w+\(self\)\s*->\s*\w+<\w+>",  # State transition
        ],
    },
    "Builder": {
        "keywords": ["Builder", "build()", "with_", "set_"],
        "patterns": [
            r"fn\s+builder\s*\(",
            r"fn\s+build\s*\(self\)",
            r"fn\s+with_\w+\s*\(self",
        ],
    },
    "Error Handling (thiserror)": {
        "imports": ["thiserror"],
        "patterns": [r"#\[derive\([^)]*Error[^)]*\)\]"],
    },
    "Error Handling (anyhow)": {
        "imports": ["anyhow"],
        "keywords": [".context(", "anyhow!", "bail!"],
    },
    "Async/Await Runtime": {
        "imports": ["tokio", "async_std", "smol"],
        "keywords": ["#[tokio::main]", "#[async_std::main]", "async fn", ".await"],
    },
    "CRDT": {
        "keywords": ["CRDT", "Replica", "Merge", "conflictfree"],
        "imports": ["crdt", "yrs", "automerge"],
    },
}


def analyze(project_path: Path) -> list[dict[str, Any]]:
    """Detect architectural patterns in a project.
    
    Filters out test/bench/example code to reduce false positives.
    """
    detected = []
    
    # Collect production Rust source code (excludes tests/benches/examples)
    all_code = ""
    for rs_file in _iter_source_files(project_path, include_tests=False):
        try:
            all_code += rs_file.read_text() + "\n"
        except Exception:
            continue
    
    # Also check Cargo.toml for dependencies
    cargo_toml = project_path / "Cargo.toml"
    cargo_content = ""
    if cargo_toml.exists():
        try:
            cargo_content = cargo_toml.read_text()
        except Exception:
            pass
    
    # Check each pattern
    for pattern_name, signatures in PATTERN_SIGNATURES.items():
        evidence = []
        score = 0
        max_score = 0
        
        # Check keywords
        keywords = signatures.get("keywords", [])
        if keywords:
            max_score += len(keywords)
            for kw in keywords:
                if kw in all_code:
                    evidence.append(f"keyword: {kw}")
                    score += 1
        
        # Check imports
        imports = signatures.get("imports", [])
        if imports:
            max_score += len(imports) * 2  # Imports are stronger signal
            for imp in imports:
                if imp in cargo_content or f"use {imp}" in all_code:
                    evidence.append(f"import: {imp}")
                    score += 2
        
        # Check patterns
        patterns = signatures.get("patterns", [])
        if patterns:
            max_score += len(patterns)
            for pat in patterns:
                if re.search(pat, all_code):
                    evidence.append(f"pattern: {pat[:30]}...")
                    score += 1
        
        # Check traits
        traits = signatures.get("traits", [])
        if traits:
            max_score += len(traits)
            for trait in traits:
                if trait in all_code:
                    evidence.append(f"trait: {trait}")
                    score += 1
        
        # Calculate confidence
        if max_score > 0 and score > 0:
            confidence = min(score / max_score, 1.0)
            if confidence >= 0.2:  # Threshold
                detected.append({
                    "name": pattern_name,
                    "confidence": confidence,
                    "evidence": evidence,
                })
    
    # Sort by confidence
    detected.sort(key=lambda x: x["confidence"], reverse=True)
    
    return detected


def export_report(patterns: list[dict[str, Any]], output: Path) -> None:
    """Export pattern detection report."""
    lines = ["# Detected Architectural Patterns", ""]
    
    if not patterns:
        lines.append("No patterns detected.")
    else:
        for p in patterns:
            lines.append(f"## {p['name']}")
            lines.append(f"**Confidence:** {p['confidence']:.0%}")
            lines.append("")
            lines.append("**Evidence:**")
            for e in p["evidence"]:
                lines.append(f"- {e}")
            lines.append("")
    
    output.write_text("\n".join(lines))
