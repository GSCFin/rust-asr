# LLM Analysis Questions Bank

Use these questions to guide deep analysis of the codebase with an LLM.

## Architecture Analysis

1. What is the primary architectural style used in this codebase? What evidence supports this conclusion?
2. How is the codebase organized? Describe the layering or modularization approach.
3. Are there any layer violations or architectural anti-patterns?
4. What are the key abstractions in this system and why were they chosen?
5. How does the error handling strategy support the overall architecture?

## Data Flow Analysis

1. Trace the data flow from input to output for the main use case.
2. Where are the primary data transformations happening?
3. How is state managed throughout the application?
4. Are there any bottlenecks in the data pipeline?
5. How does data move between different layers/modules?

## Design Patterns

1. Which design patterns are used in this codebase? Are they implemented correctly?
2. What Rust-specific idioms are leveraged (Type-State, Builder, NewType, etc.)?
3. Are there any anti-patterns that should be refactored?
4. How does the codebase leverage Rust's ownership system for safety?
5. What traits are used to abstract behavior and why?

## Concurrency & Async

1. How is concurrency handled in this codebase?
2. What async runtime is used and how is it configured?
3. Are there any potential race conditions or deadlocks?
4. How is shared state managed between concurrent tasks?
5. What synchronization primitives are used (Mutex, RwLock, channels)?

## Contributor Onboarding

1. Where should a new contributor start to understand this codebase?
2. What are the key files to read first?
3. What conventions does this project follow?
4. How should I set up my development environment?
5. What is the testing strategy and how do I run tests?

## Extension & Modification

1. How would I add a new feature to this system?
2. What extension points exist in the architecture?
3. How should new modules integrate with existing code?
4. What patterns should I follow for consistency?
5. Are there any areas that need refactoring before extending?
