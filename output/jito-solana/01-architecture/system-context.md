# System Context: jito-solana

## Overview

A Rust project

## Context Diagram

```mermaid
C4Context
title System Context Diagram for jito-solana

System(jito-solana, "jito-solana", "Rust Application")
System_Ext(serde_bytes, "serde_bytes", "External Crate")
System_Ext(tokio_tungstenite, "tokio-tungstenite", "External Crate")
System_Ext(tokio_util, "tokio-util", "External Crate")
System_Ext(tokio_serde, "tokio-serde", "External Crate")
System_Ext(serde, "serde", "External Crate")
System_Ext(tokio, "tokio", "External Crate")
System_Ext(serde_big_array, "serde-big-array", "External Crate")
System_Ext(solana_serde, "solana-serde", "External Crate")
System_Ext(serde_json, "serde_json", "External Crate")
System_Ext(serde_with, "serde_with", "External Crate")
System_Ext(axum, "axum", "External Crate")
System_Ext(tokio_stream, "tokio-stream", "External Crate")
System_Ext(hyper, "hyper", "External Crate")
System_Ext(hyper_proxy, "hyper-proxy", "External Crate")
System_Ext(serde_yaml, "serde_yaml", "External Crate")
System_Ext(solana_serde_varint, "solana-serde-varint", "External Crate")
```

## External Dependencies

| Crate | Purpose |
|-------|---------|
| `Inflector` | Third-party library |
| `aes-gcm-siv` | Third-party library |
| `affinity` | Third-party library |
| `ahash` | Third-party library |
| `anyhow` | Error handling for applications |
| `aquamarine` | Third-party library |
| `arbitrary` | Third-party library |
| `arc-swap` | Third-party library |
| `ark-bn254` | Third-party library |
| `arrayref` | Third-party library |
| `arrayvec` | Third-party library |
| `assert_cmd` | Third-party library |
| `assert_matches` | Third-party library |
| `async-lock` | Third-party library |
| `async-trait` | Async methods in traits |

## Key Capabilities

- **Multi-Crate Workspace** (90%): Multiple crates in a workspace, each with specific responsibility
- **Hexagonal/Ports-Adapters** (83%): Domain logic separated from infrastructure through traits (pluggable storage)
- **Reactor/Proactor** (83%): Async I/O with event loop (Tokio, async-std style)

### Detected Design Patterns

- **Type-State** (100%)
- **Error Handling (thiserror)** (100%)
- **Error Handling (anyhow)** (100%)
- **Builder** (86%)
- **Async/Await Runtime** (50%)