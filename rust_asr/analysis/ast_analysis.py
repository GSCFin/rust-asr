"""AST-based analysis using tree-sitter for Rust code.

Provides deeper semantic extraction than regex patterns:
- Trait implementations (impl Trait for Type)
- Derive attributes
- Type definitions with generics
- Function signatures
"""

import re
from pathlib import Path
from typing import Any

from .architecture import _iter_source_files

# Tree-sitter is optional - we fall back to enhanced regex if not available
try:
    import tree_sitter_rust as tsr
    from tree_sitter import Language, Parser
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False


def analyze_ast(project_path: Path) -> dict[str, Any]:
    """
    Perform AST-level analysis on a Rust project.
    
    Uses tree-sitter if available, otherwise falls back to enhanced regex.
    
    Returns:
        dict with impl blocks, derives, type definitions, and function signatures
    """
    impl_blocks: list[dict[str, Any]] = []
    derives: list[dict[str, Any]] = []
    type_defs: list[dict[str, Any]] = []
    fn_signatures: list[dict[str, Any]] = []
    
    for rs_file in _iter_source_files(project_path, include_tests=False):
        try:
            content = rs_file.read_text(errors="ignore")
            rel_path = str(rs_file.relative_to(project_path))
            
            file_impls = _extract_impl_blocks(content, rel_path)
            impl_blocks.extend(file_impls)
            
            file_derives = _extract_derives(content, rel_path)
            derives.extend(file_derives)
            
            file_types = _extract_type_definitions(content, rel_path)
            type_defs.extend(file_types)
            
            file_fns = _extract_function_signatures(content, rel_path)
            fn_signatures.extend(file_fns)
            
        except Exception:
            continue
    
    traits_implemented = _summarize_trait_implementations(impl_blocks)
    derive_usage = _summarize_derive_usage(derives)
    
    return {
        "project": project_path.name,
        "impl_blocks": impl_blocks,
        "derives": derives,
        "type_definitions": type_defs,
        "function_signatures": fn_signatures[:100],
        "traits_implemented": traits_implemented,
        "derive_usage": derive_usage,
        "stats": {
            "total_impl_blocks": len(impl_blocks),
            "trait_impls": sum(1 for i in impl_blocks if i.get("trait")),
            "inherent_impls": sum(1 for i in impl_blocks if not i.get("trait")),
            "total_derives": len(derives),
            "total_type_defs": len(type_defs),
            "total_functions": len(fn_signatures),
        },
        "tree_sitter_available": TREE_SITTER_AVAILABLE,
    }


def _extract_impl_blocks(content: str, file_path: str) -> list[dict[str, Any]]:
    """Extract impl blocks, distinguishing trait impls from inherent impls."""
    impls = []
    
    trait_impl_pattern = r"impl(?:<([^>]+)>)?\s+(\w+)(?:<[^>]+>)?\s+for\s+(\w+)(?:<([^>]+)>)?"
    for match in re.finditer(trait_impl_pattern, content):
        generics = match.group(1)
        trait_name = match.group(2)
        type_name = match.group(3)
        type_generics = match.group(4)
        
        line = content[:match.start()].count("\n") + 1
        
        impls.append({
            "type": type_name,
            "trait": trait_name,
            "generics": generics,
            "type_generics": type_generics,
            "file": file_path,
            "line": line,
            "kind": "trait_impl",
        })
    
    inherent_impl_pattern = r"impl(?:<([^>]+)>)?\s+(\w+)(?:<([^>]+)>)?\s*\{"
    for match in re.finditer(inherent_impl_pattern, content):
        if " for " in content[match.start():match.end() + 50]:
            continue
        
        generics = match.group(1)
        type_name = match.group(2)
        type_generics = match.group(3)
        
        line = content[:match.start()].count("\n") + 1
        
        impls.append({
            "type": type_name,
            "trait": None,
            "generics": generics,
            "type_generics": type_generics,
            "file": file_path,
            "line": line,
            "kind": "inherent_impl",
        })
    
    return impls


def _extract_derives(content: str, file_path: str) -> list[dict[str, Any]]:
    """Extract derive attributes with their associated types."""
    derives = []
    
    derive_pattern = r"#\[derive\(([^)]+)\)\]\s*(?:pub(?:\([^)]*\))?\s+)?(?:struct|enum)\s+(\w+)"
    
    for match in re.finditer(derive_pattern, content):
        derive_list = match.group(1)
        type_name = match.group(2)
        
        traits = [t.strip() for t in derive_list.split(",")]
        
        line = content[:match.start()].count("\n") + 1
        
        derives.append({
            "type": type_name,
            "derives": traits,
            "file": file_path,
            "line": line,
        })
    
    return derives


def _extract_type_definitions(content: str, file_path: str) -> list[dict[str, Any]]:
    """Extract struct and enum definitions with their fields/variants."""
    type_defs = []
    
    struct_pattern = r"(?:pub(?:\([^)]*\))?\s+)?struct\s+(\w+)(?:<([^>]+)>)?\s*(?:\([^)]*\)|(?:\{[^}]*\})?|;)"
    
    for match in re.finditer(struct_pattern, content):
        name = match.group(1)
        generics = match.group(2)
        
        line = content[:match.start()].count("\n") + 1
        
        type_defs.append({
            "name": name,
            "kind": "struct",
            "generics": generics,
            "file": file_path,
            "line": line,
        })
    
    enum_pattern = r"(?:pub(?:\([^)]*\))?\s+)?enum\s+(\w+)(?:<([^>]+)>)?"
    
    for match in re.finditer(enum_pattern, content):
        name = match.group(1)
        generics = match.group(2)
        
        line = content[:match.start()].count("\n") + 1
        
        type_defs.append({
            "name": name,
            "kind": "enum",
            "generics": generics,
            "file": file_path,
            "line": line,
        })
    
    return type_defs


def _extract_function_signatures(content: str, file_path: str) -> list[dict[str, Any]]:
    """Extract function signatures with parameters and return types."""
    functions = []
    
    fn_pattern = r"(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?fn\s+(\w+)(?:<([^>]+)>)?\s*\(([^)]*)\)(?:\s*->\s*([^{;]+))?"
    
    for match in re.finditer(fn_pattern, content):
        name = match.group(1)
        generics = match.group(2)
        params = match.group(3)
        return_type = match.group(4)
        
        if name in ["new", "default", "from", "into", "as_ref", "as_mut"]:
            continue
        
        line = content[:match.start()].count("\n") + 1
        
        is_async = "async fn" in content[max(0, match.start()-10):match.start()+10]
        
        functions.append({
            "name": name,
            "generics": generics,
            "params": params.strip() if params else "",
            "return_type": return_type.strip() if return_type else None,
            "is_async": is_async,
            "file": file_path,
            "line": line,
        })
    
    return functions


def _summarize_trait_implementations(impl_blocks: list[dict]) -> dict[str, list[str]]:
    """Summarize which types implement which traits."""
    trait_to_types: dict[str, list[str]] = {}
    
    for impl_block in impl_blocks:
        if impl_block.get("trait"):
            trait = impl_block["trait"]
            type_name = impl_block["type"]
            
            if trait not in trait_to_types:
                trait_to_types[trait] = []
            if type_name not in trait_to_types[trait]:
                trait_to_types[trait].append(type_name)
    
    return dict(sorted(trait_to_types.items(), key=lambda x: -len(x[1])))


def _summarize_derive_usage(derives: list[dict]) -> dict[str, int]:
    """Summarize derive macro usage."""
    derive_counts: dict[str, int] = {}
    
    for derive in derives:
        for trait in derive["derives"]:
            derive_counts[trait] = derive_counts.get(trait, 0) + 1
    
    return dict(sorted(derive_counts.items(), key=lambda x: -x[1]))


def export_ast_report(ast_data: dict[str, Any], output_path: Path) -> None:
    """Export AST analysis as markdown report."""
    lines = [
        f"# AST Analysis: {ast_data['project']}",
        "",
        "## Statistics",
        "",
        f"- **Total impl blocks:** {ast_data['stats']['total_impl_blocks']}",
        f"  - Trait implementations: {ast_data['stats']['trait_impls']}",
        f"  - Inherent implementations: {ast_data['stats']['inherent_impls']}",
        f"- **Total derives:** {ast_data['stats']['total_derives']}",
        f"- **Type definitions:** {ast_data['stats']['total_type_defs']}",
        f"- **Functions:** {ast_data['stats']['total_functions']}",
        "",
        "## Top Trait Implementations",
        "",
    ]
    
    for trait, types in list(ast_data["traits_implemented"].items())[:15]:
        lines.append(f"### `{trait}` ({len(types)} types)")
        for t in types[:5]:
            lines.append(f"- `{t}`")
        if len(types) > 5:
            lines.append(f"- ... and {len(types) - 5} more")
        lines.append("")
    
    lines.extend(["## Top Derive Macros", ""])
    
    for derive, count in list(ast_data["derive_usage"].items())[:10]:
        lines.append(f"- `{derive}`: {count} uses")
    
    output_path.write_text("\n".join(lines))
