# Getting Started: jito-solana

## Prerequisites

- Rust 1.70+ (with `cargo`)
- Git

## Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_ORG/jito-solana.git
cd jito-solana

# Build
cargo build --release

# Run tests
cargo test
```

## Building

### Debug Build

```bash
cargo build
```

### Release Build

```bash
cargo build --release
```

## Feature Flags

```bash
# Build with all features
cargo build --all-features

# Build with specific feature
cargo build --features feature_name
```