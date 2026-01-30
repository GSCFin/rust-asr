# Public APIs: jito-solana

## Entry Points

| Function | Parameters | Returns | File |
|----------|------------|---------|------|
| `all_enabled` | 0 | `Self` | svm-feature-set/src/lib.rs |
| `should_track_transaction` | 1 | `bool` | transaction-metrics-tracker/src/lib.rs |
| `signature_if_should_track_packet` | 2 | `Result<Option<&[u8` | transaction-metrics-tracker/src/lib.rs |
| `get_signature_from_packet` | 2 | `Result<&[u8` | transaction-metrics-tracker/src/lib.rs |
| `new_as_boxed` | 1 | `Box<Self>` | clap-utils/src/lib.rs |
| `hidden_unless_forced` | 0 | `bool` | clap-utils/src/lib.rs |
| `create_program_runtime_environment_v1` | 5 | `Result<BuiltinProgram<InvokeCo` | syscalls/src/lib.rs |
| `create_program_runtime_environment_v2` | 3 | `BuiltinProgram<InvokeContext<'` | syscalls/src/lib.rs |
| `get_public_ip_addr_with_binding` | 3 | `anyhow::Result<IpAddr>` | net-utils/src/lib.rs |
| `get_cluster_shred_version` | 1 | `Result<u16, String>` | net-utils/src/lib.rs |

## Public Functions

| Function | Parameters | Returns | File |
|----------|------------|---------|------|
| `get_cli_config` | 1 | `CliConfig<'_>` | cargo-registry/src/client.rs |
| `new` | 1 | `Self` | remote-wallet/src/ledger.rs |
| `get_settings` | 0 | `Result<LedgerSettings, RemoteW` | remote-wallet/src/ledger.rs |
| `is_valid_ledger` | 2 | `bool` | remote-wallet/src/ledger.rs |
| `get_ledger_from_info` | 4 | `Result<Rc<LedgerWallet>, Remot` | remote-wallet/src/ledger.rs |
| `new_from_uri` | 1 | `Result<Self, LocatorError>` | remote-wallet/src/locator.rs |
| `new_from_parts` | 3 | `Result<Self, LocatorError>
   ` | remote-wallet/src/locator.rs |
| `new` | 1 | `Rc<Self>` | remote-wallet/src/remote_wallet.rs |
| `update_devices` | 0 | `Result<usize, RemoteWalletErro` | remote-wallet/src/remote_wallet.rs |
| `update_devices` | 0 | `Result<usize, RemoteWalletErro` | remote-wallet/src/remote_wallet.rs |
| `list_devices` | 0 | `Vec<RemoteWalletInfo>` | remote-wallet/src/remote_wallet.rs |
| `get_ledger` | 3 | `Result<Rc<LedgerWallet>, Remot` | remote-wallet/src/remote_wallet.rs |
| `get_wallet_info` | 2 | `Option<RemoteWalletInfo>` | remote-wallet/src/remote_wallet.rs |
| `try_connect_polling` | 2 | `bool` | remote-wallet/src/remote_wallet.rs |
| `parse_locator` | 1 | `Self` | remote-wallet/src/remote_wallet.rs |
| `get_pretty_path` | 0 | `String` | remote-wallet/src/remote_wallet.rs |
| `is_valid_hid_device` | 2 | `bool` | remote-wallet/src/remote_wallet.rs |
| `initialize_wallet_manager` | 0 | `Result<Rc<RemoteWalletManager>` | remote-wallet/src/remote_wallet.rs |
| `initialize_wallet_manager` | 0 | `Result<Rc<RemoteWalletManager>` | remote-wallet/src/remote_wallet.rs |
| `maybe_wallet_manager` | 0 | `Result<Option<Rc<RemoteWalletM` | remote-wallet/src/remote_wallet.rs |