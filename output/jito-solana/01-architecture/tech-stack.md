# Tech Stack: jito-solana

## Rust Configuration

- **Edition**: 2021
- **Toolchain**: 1.90.0

## Core Dependencies

| Crate | Purpose |
|-------|---------|
| `anyhow` | Application error handling |
| `axum` | Ergonomic web framework |
| `bytes` | Byte buffer utilities |
| `clap` | Command-line argument parsing |
| `hyper` | HTTP implementation |
| `log` | Logging facade |
| `parking_lot` | Fast synchronization |
| `rayon` | Data parallelism |
| `regex` | Regular expressions |
| `serde` | Serialization/deserialization framework |
| `serde_json` | JSON support for serde |
| `thiserror` | Library error types |
| `tokio` | Async runtime with work-stealing scheduler |
| `tracing` | Instrumentation and logging |
| `Inflector` | Third-party dependency |
| `aes-gcm-siv` | Third-party dependency |
| `affinity` | Third-party dependency |
| `agave-banking-stage-ingress-types` | Third-party dependency |
| `agave-feature-set` | Third-party dependency |

## Feature Flags

| Feature | Crate | Dependencies |
|---------|-------|--------------|

## Workspace Structure (142 crates)

| Crate | Dependencies | Description |
|-------|--------------|-------------|
| `solana-account-decoder` | 39 | Solana account decoder |
| `solana-account-decoder-client-types` | 7 | Core RPC client types for solana-account |
| `solana-accounts-cluster-bench` | 39 | - |
| `agave-logger` | 4 | Agave Logger |
| `solana-clap-utils` | 26 | Solana utilities for the clap |
| `solana-remote-wallet` | 18 | Blockchain, Rebuilt for Scale |
| `solana-cli-config` | 7 | Blockchain, Rebuilt for Scale |
| `solana-client` | 41 | Solana Client |
| `solana-connection-cache` | 19 | Solana Connection Cache |
| `solana-measure` | 0 | Blockchain, Rebuilt for Scale |
| `solana-metrics` | 14 | Solana Metrics |
| `solana-net-utils` | 20 | Solana Network Utilities |
| `solana-svm-type-overrides` | 3 | Type overrides for specialized testing |
| `solana-pubsub-client` | 21 | Solana Pubsub Client |
| `solana-rpc-client-types` | 21 | Solana RPC Client Types |
| `solana-transaction-status-client-types` | 17 | Core RPC client types for solana-transac |
| `solana-transaction-context` | 16 | Solana data shared between program runti |
| `solana-version` | 8 | Solana Version |
| `agave-feature-set` | 8 | Solana runtime feature declarations |
| `solana-svm-feature-set` | 0 | Solana SVM Feature Set |