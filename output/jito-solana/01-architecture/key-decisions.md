# Key Architectural Decisions: jito-solana

> These ADRs are inferred from code patterns. Manual validation recommended.

## ADR-001: Adopt Multi-Crate Workspace

**Status**: Inferred (Confidence: 90%)

### Context

The project requires multiple crates in a workspace, each with specific responsibility.

### Decision

Use Multi-Crate Workspace architecture pattern.

### Evidence

- Workspace with 142 packages

### Consequences

- Improved code organization
- Clear separation of concerns

---

## ADR-002: Adopt Hexagonal/Ports-Adapters

**Status**: Inferred (Confidence: 83%)

### Context

The project requires domain logic separated from infrastructure through traits (pluggable storage).

### Decision

Use Hexagonal/Ports-Adapters architecture pattern.

### Evidence

- port
- adapter
- domain
- Storage
- Backend

### Consequences

- Improved code organization
- Clear separation of concerns

---

## ADR-003: Adopt Reactor/Proactor

**Status**: Inferred (Confidence: 83%)

### Context

The project requires async i/o with event loop (tokio, async-std style).

### Decision

Use Reactor/Proactor architecture pattern.

### Evidence

- Future
- Poll::
- async fn
- .await
- executor

### Consequences

- Improved code organization
- Clear separation of concerns

---

## ADR-004: Adopt Work-Stealing Scheduler

**Status**: Inferred (Confidence: 75%)

### Context

The project requires load-balanced task scheduling across worker threads.

### Decision

Use Work-Stealing Scheduler architecture pattern.

### Evidence

- multi_thread
- Runtime::new
- tokio::runtime

### Consequences

- Improved code organization
- Clear separation of concerns

---

## ADR-005: Adopt Event-Driven

**Status**: Inferred (Confidence: 60%)

### Context

The project requires components communicate through events and messages.

### Decision

Use Event-Driven architecture pattern.

### Evidence

- Event
- on_event
- emit

### Consequences

- Improved code organization
- Clear separation of concerns

---

## ADR-006: Adopt Plugin Architecture

**Status**: Inferred (Confidence: 50%)

### Context

The project requires core system with extensible plugin-based functionality.

### Decision

Use Plugin Architecture architecture pattern.

### Evidence

- plugin
- Plugin

### Consequences

- Improved code organization
- Clear separation of concerns

---

## ADR-007: Use Shared State (RwLock)

**Status**: Inferred (Usage Count: 1081)

### Context

Components need safe, concurrent communication.

### Decision

Adopt Shared State (RwLock) for inter-component messaging.

### Evidence

- `Arc<RwLock`
- `RwLock<`
- `std::sync::RwLock`

### Consequences

- Thread-safe by design
- Decoupled components

---

## ADR-008: Use Shared State (Mutex)

**Status**: Inferred (Usage Count: 306)

### Context

Components need safe, concurrent communication.

### Decision

Adopt Shared State (Mutex) for inter-component messaging.

### Evidence

- `Arc<Mutex`
- `Mutex<`
- `std::sync::Mutex`

### Consequences

- Thread-safe by design
- Decoupled components

---

## ADR-009: Apply Type-State Pattern

**Status**: Inferred (Confidence: 100%)

### Context

The codebase applies the Type-State pattern.

### Evidence

- pattern: struct\s+\w+<\w+>...
- pattern: impl\s+\w+<\w+>...
- pattern: fn\s+\w+\(self\)\s*->\s*\w+<\w...

---

## ADR-010: Apply Error Handling (thiserror) Pattern

**Status**: Inferred (Confidence: 100%)

### Context

The codebase applies the Error Handling (thiserror) pattern.

### Evidence

- import: thiserror
- pattern: #\[derive\([^)]*Error[^)]*\)\]...

---

## ADR-011: Apply Error Handling (anyhow) Pattern

**Status**: Inferred (Confidence: 100%)

### Context

The codebase applies the Error Handling (anyhow) pattern.

### Evidence

- keyword: .context(
- keyword: anyhow!
- keyword: bail!

---
