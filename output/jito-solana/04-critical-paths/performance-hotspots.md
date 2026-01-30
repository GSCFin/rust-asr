# Performance Hotspots: jito-solana

## Observability Status

- **Tracing enabled**: ✅ 
- **Tokio tracing**: ✅
- **Instrumented functions**: 0

## Recommendations

No instrumented functions detected. Consider adding:

```rust
#[tracing::instrument]
pub fn critical_function() {
    // ...
}
```

## Flamegraph Analysis

To generate flamegraph for runtime analysis:

```bash
cargo install flamegraph
cargo flamegraph --bin jito-solana
```

> Generated flamegraph.svg can reveal CPU hotspots.