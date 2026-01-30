# Semantic Index: jito-solana

## Quick Navigation Guide

### Entry Points
Start here to understand the codebase:
- **install/build.rs** - main() function

### Hot Spots (Most Connected)
Key components with many relationships:
- `field_usage` (9960 connections)
- `Debug` (1189 connections)
- `lib` (1109 connections)
- `Clone` (783 connections)
- `PartialEq` (651 connections)
- `Default` (567 connections)
- `tests` (436 connections)
- `Eq` (419 connections)
- `rpc_client` (381 connections)
- `RpcClient` (341 connections)

### Public APIs
Exported interfaces:
- `get_cli_config` (fn) in `cargo-registry/src/client.rs`
- `CargoRegistryService` (struct) in `cargo-registry/src/main.rs`
- `SVMFeatureSet` (struct) in `svm-feature-set/src/lib.rs`
- `all_enabled` (fn) in `svm-feature-set/src/lib.rs`
- `should_track_transaction` (fn) in `transaction-metrics-tracker/src/lib.rs`
- `signature_if_should_track_packet` (fn) in `transaction-metrics-tracker/src/lib.rs`
- `get_signature_from_packet` (fn) in `transaction-metrics-tracker/src/lib.rs`
- `LedgerSettings` (struct) in `remote-wallet/src/ledger.rs`
- `LedgerWallet` (struct) in `remote-wallet/src/ledger.rs`
- `get_settings` (fn) in `remote-wallet/src/ledger.rs`
- `is_valid_ledger` (fn) in `remote-wallet/src/ledger.rs`
- `get_ledger_from_info` (fn) in `remote-wallet/src/ledger.rs`
- `ManufacturerError` (struct) in `remote-wallet/src/locator.rs`
- `Locator` (struct) in `remote-wallet/src/locator.rs`
- `new_from_path` (fn) in `remote-wallet/src/locator.rs`
- ... and 35 more

### File Overview
- Total files with entities: 1126
- Total named concepts: 15441
- Total public APIs: 4844