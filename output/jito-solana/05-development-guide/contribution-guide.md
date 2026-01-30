# Contributing to jito-solana

## Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and commit: `git commit -m 'Add feature'`
4. Push to your fork: `git push origin feature/my-feature`
5. Open a Pull Request

## Before Submitting

```bash
# Format code
cargo fmt

# Run linter
cargo clippy -- -D warnings

# Run tests
cargo test
```

## Commit Message Format

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code change without new feature or fix
- `test:` Adding tests

## Code Review Process

1. All PRs require at least one approval
2. CI must pass (fmt, clippy, tests)
3. Maintain test coverage