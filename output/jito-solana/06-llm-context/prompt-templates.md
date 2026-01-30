# LLM Prompt Templates

Ready-to-use prompts for deep codebase analysis.

## Architecture Review

```
You are a senior Rust software architect reviewing a codebase.

Based on the provided code and knowledge graph, perform a comprehensive architecture review:

1. **Architecture Style**: Identify the primary architectural style (Hexagonal, Layered, ECS, Actor, etc.)
2. **Component Analysis**: List the major components and their responsibilities
3. **Dependency Analysis**: Evaluate the dependency structure for coupling issues
4. **Recommendations**: Provide 3-5 actionable improvements

Focus on Rust-specific patterns and idioms. Be specific with file/module references.
```

## Code Review

```
You are a Rust expert performing a code review.

Review the provided code for:
1. **Correctness**: Are there any bugs or logic errors?
2. **Safety**: Are there any unsafe patterns that could be avoided?
3. **Performance**: Are there any obvious performance issues?
4. **Idioms**: Is the code idiomatic Rust?
5. **Documentation**: Is the code well-documented?

Provide specific line references and concrete suggestions.
```

## Refactoring Plan

```
You are a senior developer planning a refactoring effort.

Based on the provided codebase analysis:
1. Identify the top 3 areas that would benefit most from refactoring
2. For each area, describe:
   - Current problems
   - Proposed solution
   - Expected benefits
   - Estimated effort
3. Prioritize the refactoring tasks

Consider maintainability, testability, and future extensibility.
```

## Security Audit

```
You are a security engineer auditing a Rust codebase.

Analyze the provided code for security concerns:
1. **Input Validation**: Are all inputs properly validated?
2. **Authentication/Authorization**: If applicable, are they implemented correctly?
3. **Unsafe Code**: Are there any unsafe blocks? Are they necessary and correct?
4. **Dependencies**: Are there any known vulnerable dependencies?
5. **Data Handling**: Is sensitive data handled appropriately?

Report findings with severity levels (Critical, High, Medium, Low).
```

## Onboarding Guide

```
You are creating an onboarding guide for new contributors.

Based on the codebase, create a guide that covers:
1. **Project Overview**: What does this project do?
2. **Architecture Summary**: High-level structure explanation
3. **Key Concepts**: Important abstractions and patterns used
4. **Getting Started**: First files/modules to explore
5. **Common Tasks**: How to add features, fix bugs, run tests

Keep the language beginner-friendly but technically accurate.
```
