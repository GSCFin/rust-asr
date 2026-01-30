# Code Conventions: jito-solana

## Rust Style

This project follows standard Rust conventions:

- **Naming**: `snake_case` for functions/variables, `CamelCase` for types
- **Formatting**: `cargo fmt` (rustfmt default)
- **Linting**: `cargo clippy` with default configuration

## Pre-Commit Checks

```bash
cargo fmt --check
cargo clippy -- -D warnings
cargo test
```

## Design Patterns Used

- **Type-State** (100%)
- **Error Handling (thiserror)** (100%)
- **Error Handling (anyhow)** (100%)
- **Builder** (86%)
- **Async/Await Runtime** (50%)

## Architecture Guidelines

- **Multi-Crate Workspace**: Multiple crates in a workspace, each with specific responsibility
- **Hexagonal/Ports-Adapters**: Domain logic separated from infrastructure through traits (pluggable storage)

## Error Handling

- Use `Result<T, E>` for fallible operations
- Prefer `?` operator over `.unwrap()`
- Use `anyhow` for application errors
- Use `thiserror` for library error types