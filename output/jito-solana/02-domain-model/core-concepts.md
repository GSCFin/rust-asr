# Core Concepts: jito-solana

## Domain Entities

### Key Data Structures

| Struct | Fields | File |
|--------|--------|------|
| `CargoRegistryService` |  | cargo-registry/src/main.rs |
| `SVMFeatureSet` | pub move_precompile_verification_to_svm, pub stricter_abi_and_runtime_constraints, pub account_data_direct_mapping... | svm-feature-set/src/lib.rs |
| `LedgerSettings` | pub enable_blind_signing, pub pubkey_display | remote-wallet/src/ledger.rs |
| `LedgerWallet` | #[cfg(feature = "hidapi")]
    pub device, pub pretty_path, pub version | remote-wallet/src/ledger.rs |
| `Locator` | pub manufacturer, pub pubkey | remote-wallet/src/locator.rs |
| `RemoteWalletManager` | #[cfg(feature = "hidapi")]
    usb, devices | remote-wallet/src/remote_wallet.rs |
| `Device` | pub(crate) path, pub(crate) info, pub wallet_type | remote-wallet/src/remote_wallet.rs |
| `RemoteWalletInfo` | /// RemoteWallet device model
    pub model, /// RemoteWallet device manufacturer
    pub manufacturer, /// RemoteWallet device serial number
    pub serial... | remote-wallet/src/remote_wallet.rs |
| `RemoteKeypair` | pub wallet_type, pub derivation_path, pub pubkey... | remote-wallet/src/remote_keypair.rs |
| `ArgConstant` | pub long, pub name, pub help | clap-utils/src/lib.rs |
| `SignOnly` | pub blockhash, pub message, pub present_signers... | clap-utils/src/keypair.rs |
| `CliSignerInfo` | pub signers | clap-utils/src/keypair.rs |
| `DefaultSigner` | /// The name of the signers command line argument.
    pub arg_name, /// The signing source.
    pub path, is_path_checked | clap-utils/src/keypair.rs |
| `SignerFromPathConfig` | pub allow_null_signer | clap-utils/src/keypair.rs |
| `PubkeysPtr` | ptr, count | scheduling-utils/src/pubkeys_ptr.rs |

### Enumerations

| Enum | Variants | File |
|------|----------|------|
| `PubkeyDisplayMode` | Short, Long | remote-wallet/src/ledger.rs |
| `Manufacturer` | #[default]
    Unknown, Ledger | remote-wallet/src/locator.rs |
| `LocatorError` | #[error, #[error, #[error... | remote-wallet/src/locator.rs |
| `LedgerError` | #[error, #[error, #[error... | remote-wallet/src/ledger_error.rs |
| `RemoteWalletError` | #[error | remote-wallet/src/remote_wallet.rs |
| `RemoteWalletType` | Ledger | remote-wallet/src/remote_wallet.rs |
| `ComputeUnitLimit` | which will give the
    /// transaction a compute unit limit of:
    /// `min, 200_000 * | clap-utils/src/compute_budget.rs |
| `TryLockError` |  | scheduling-utils/src/thread_aware_account_locks.rs |
| `ClientHandshakeError` | #[error | scheduling-utils/src/handshake/client.rs |
| `AgaveHandshakeError` | #[error | scheduling-utils/src/handshake/server.rs |

### Core Traits

| Trait | File |
|-------|------|
| `RemoteWallet` | remote-wallet/src/remote_wallet.rs |
| `ArgsConfig` | clap-utils/src/offline.rs |
| `OfflineArgs` | clap-utils/src/offline.rs |
| `NonceArgs` | clap-utils/src/nonce.rs |
| `PointValidation` | curves/curve25519/src/curve_syscall_traits.rs |
| `GroupOperations` | curves/curve25519/src/curve_syscall_traits.rs |
| `MultiScalarMultiplication` | curves/curve25519/src/curve_syscall_traits.rs |
| `Pairing` | curves/curve25519/src/curve_syscall_traits.rs |
| `SocketProvider` | net-utils/src/multihomed_sockets.rs |
| `ProgramTestBanksClientExt` | program-test/src/lib.rs |

## Entity Relationships

```mermaid
erDiagram
    SVMFeatureSet ||--o| move_precompile_verification_to_svm : contains
    SVMFeatureSet ||--o| stricter_abi_and_runtime_constraints : contains
    SVMFeatureSet ||--o| account_data_direct_mapping : contains
    LedgerSettings ||--o| enable_blind_signing : contains
    LedgerSettings ||--o| pubkey_display : contains
    LedgerWallet ||--o| #[cfg(feature = "hidapi")]
    device : contains
    LedgerWallet ||--o| pretty_path : contains
    LedgerWallet ||--o| version : contains
    Locator ||--o| manufacturer : contains
    Locator ||--o| pubkey : contains
    RemoteWalletManager ||--o| #[cfg(feature = "hidapi")]
    usb : contains
    RemoteWalletManager ||--o| devices : contains
    Device ||--o| pub(crate) path : contains
    Device ||--o| pub(crate) info : contains
    Device ||--o| wallet_type : contains
    RemoteWalletInfo ||--o| /// RemoteWallet device model
    model : contains
    RemoteWalletInfo ||--o| /// RemoteWallet device manufacturer
    manufacturer : contains
    RemoteWalletInfo ||--o| /// RemoteWallet device serial number
    serial : contains
```