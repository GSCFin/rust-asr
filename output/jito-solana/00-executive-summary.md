# jito-solana

## At a Glance

> A Rust project

| Attribute | Value |
|-----------|-------|
| **Edition** | Rust 2021 |
| **Crates** | 142 |
| **Tech Focus** | Serialization (`serde`), Serialization (`serde`), CLI (`clap`), Parallelism (`rayon`), CLI (`clap`) |

## Architecture

**Primary Style:** Multi-Crate Workspace (90% confidence)

Multiple crates in a workspace, each with specific responsibility

## Key Decisions

- ✅ **Multi-Crate Workspace** architecture pattern
- ✅ **Hexagonal/Ports-Adapters** architecture pattern
- ✅ **Type-State** design pattern
- ✅ **Error Handling (thiserror)** design pattern

## Documentation

| Section | Description |
|---------|-------------|
| [01-architecture](01-architecture/) | System context, design, decisions |
| [02-domain-model](02-domain-model/) | Core concepts and data models |
| [03-api-interfaces](03-api-interfaces/) | Public APIs and contracts |
| [04-critical-paths](04-critical-paths/) | Main flows and hotspots |
| [05-development-guide](05-development-guide/) | Getting started and conventions |