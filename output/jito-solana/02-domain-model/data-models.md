# Data Models: jito-solana

## Type Aliases

| Alias | Definition | File |
|-------|------------|------|
| `CliSigners` | `Vec<Box<dyn Signer>>` | clap-utils/src/keypair.rs |
| `SignerIndex` | `usize` | clap-utils/src/keypair.rs |
| `ThreadId` | `usize` | scheduling-utils/src/thread_aware_account_locks.rs |
| `IpEchoServer` | `Runtime` | net-utils/src/ip_echo_server.rs |
| `PortRange` | `(u16, u16)` | net-utils/src/lib.rs |
| `BankingPacketBatch` | `Arc<Vec<PacketBatch>>` | banking-stage-ingress-types/src/lib.rs |
| `BankingPacketReceiver` | `Receiver<BankingPacketBatch>` | banking-stage-ingress-types/src/lib.rs |
| `AsyncTryJoinHandle` | `TryJoin<JoinHandle<()>, JoinHandle<()>>` | turbine/src/quic_endpoint.rs |
| `OrderedTaskId` | `u128` | unified-scheduler-logic/src/lib.rs |
| `Task` | `Arc<TaskInner>` | unified-scheduler-logic/src/lib.rs |

## Key Structures (Detailed)

### `CargoRegistryService`

*From: cargo-registry/src/main.rs*

**Fields:**

### `SVMFeatureSet`

*From: svm-feature-set/src/lib.rs*

**Fields:**
- `pub move_precompile_verification_to_svm`
- `pub stricter_abi_and_runtime_constraints`
- `pub account_data_direct_mapping`
- `pub enable_bpf_loader_set_authority_checked_ix`
- `pub enable_loader_v4`

### `LedgerSettings`

*From: remote-wallet/src/ledger.rs*

**Fields:**
- `pub enable_blind_signing`
- `pub pubkey_display`

### `LedgerWallet`

*From: remote-wallet/src/ledger.rs*

**Fields:**
- `#[cfg(feature = "hidapi")]
    pub device`
- `pub pretty_path`
- `pub version`

### `Locator`

*From: remote-wallet/src/locator.rs*

**Fields:**
- `pub manufacturer`
- `pub pubkey`
