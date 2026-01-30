<p align="center">
  <img src="https://img.shields.io/badge/Rust-Software%20Architecture%20Recovery-orange?style=for-the-badge&logo=rust" alt="Rust ASR">
</p>

<h1 align="center">🦀 Rust ASR</h1>

<p align="center">
  <strong>Software Architecture Recovery Toolkit for Rust Projects</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#example-output">Example Output</a> •
  <a href="#cli-reference">CLI Reference</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <a href="README_VI.md">🇻🇳 Tiếng Việt</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/AI-Gemini%20Powered-purple.svg" alt="AI Powered">
</p>

> [!WARNING]
> **🚧 Project Status: Under Active Development**
>
> This project is still in the early development phase. Many tools and analysis modules need further refinement. Contributions and feedback are welcome!

---

A comprehensive Python toolkit for extracting architectural knowledge from Rust projects. Generate **PM-ready documentation**, **C4 diagrams**, **knowledge graphs**, and **LLM-optimized context** — all from static analysis with zero runtime requirements.

## Features

### 📊 Static Analysis (Zero LLM)

| Feature                    | Description                                                 |
| -------------------------- | ----------------------------------------------------------- |
| **Dependency Graph**       | Analyze crate dependencies, identify core components        |
| **Module Structure**       | Map visibility boundaries (`pub` vs `pub(crate)`)           |
| **Pattern Recognition**    | Detect Tower Service, ECS, Type-State, Builder patterns     |
| **Architecture Styles**    | Hexagonal, Actor Model, Plugin, Multi-Crate Workspace       |
| **Communication Patterns** | Channel-based, Shared State (Mutex/RwLock), Message Passing |

### 🤖 AI-Enhanced Analysis (Gemini)

| Feature              | Description                                          |
| -------------------- | ---------------------------------------------------- |
| **C4 Diagrams**      | Auto-generate Context, Container, Component diagrams |
| **ADR Extraction**   | Infer Architectural Decision Records from code       |
| **Deployment Model** | Analyze runtime requirements and scaling patterns    |

### 📚 Documentation Export (5+1 Structure)

Generate **18+ files** across 6 sections:

```
output/
├── 00-executive-summary.md      # TL;DR, tech stack, key decisions
├── 01-architecture/             # C4 diagrams, styles, ADRs
├── 02-domain-model/             # Entities, types, data flow
├── 03-api-interfaces/           # Public APIs, contracts
├── 04-critical-paths/           # Main flows, error handling
├── 05-development-guide/        # Getting started, conventions
└── 06-llm-context/              # Knowledge graph, codebase chunks
```

### 🧠 LLM Context Generation

For AI-assisted development and architecture understanding:

| Output               | Description                                     |
| -------------------- | ----------------------------------------------- |
| **Codebase Chunks**  | Split codebase into ~2MB parts via repomix      |
| **Knowledge Graph**  | Entity relationships with 15K+ nodes            |
| **Semantic Index**   | Navigation guide for codebase exploration       |
| **Pattern Library**  | Documented design patterns with examples        |
| **Prompt Templates** | Ready-to-use prompts for architecture questions |

---

## Installation

### Requirements

- Python 3.10+
- [repomix](https://github.com/yamadashy/repomix) (for LLM context generation)

### Install from source

```bash
# Clone the repository
git clone https://github.com/your-org/rust-asr.git
cd rust-asr

# Install with pip (editable mode)
pip install -e .

# For AI features (optional)
pip install -e ".[ai]"
```

### Configure AI (Optional)

```bash
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY
```

**.env example:**

```bash
GOOGLE_API_KEY=your_api_key_here
GOOGLE_API_URL=https://generativelanguage.googleapis.com/v1beta/openai
GOOGLE_MODEL=gemini-2.0-flash
```

---

## Quick Start

### Fetch Champion Projects

```bash
# Download curated Rust projects for analysis
rust-asr fetch --champions
```

### Generate Full Documentation

```bash
# Basic documentation (18 files, 0 LLM requests)
rust-asr docs --path ./repos/tokio --output ./output/tokio

# With LLM context section (knowledge graph, codebase chunks)
rust-asr docs --path ./repos/jito-solana --output ./output/jito-solana --with-llm-context

# With AI-enhanced ADRs
rust-asr docs --path ./repos/bevy --output ./output/bevy --with-ai
```

### Pattern Detection

```bash
rust-asr patterns --path ./repos/zed
```

### Architecture Analysis

```bash
rust-asr architecture --path ./repos/ripgrep --output ./analysis
```

---

## Example Output

### Case Study: jito-solana (Solana Blockchain Fork)

Running full "cold" analysis on the jito-solana codebase:

```bash
$ rust-asr docs -p repos/jito-solana -o output/jito-solana --with-llm-context

╭── 📄 Architecture Docs Export ──╮
│ Generating Documentation:       │
│ jito-solana                     │
╰─────────────────────────────────╯
Sections: api, architecture, dev, domain, llm-context, paths, summary

Running analysis...
✓ Analysis complete

Generating 01-architecture/
Generating 02-domain-model/
Generating 03-api-interfaces/
Generating 04-critical-paths/
Generating 05-development-guide/
Generating 06-llm-context/
  Exporting codebase with repomix...
  ✓ 5 file(s), repomix_split
  Building knowledge graph...
  ✓ 15441 nodes, 18930 edges
  Building semantic index...
  ✓ Semantic index complete
  Building pattern library...
  ✓ 7 patterns documented
  Exporting prompts & questions...
  ✓ Prompts exported
Generating 00-executive-summary.md

✓ Documentation saved to: output/jito-solana
```

### Generated Structure

```
output/jito-solana/
├── 00-executive-summary.md           (1.0 KB)
├── 01-architecture/
│   ├── high-level-design.md          (4.4 KB)
│   ├── key-decisions.md              (3.8 KB)
│   ├── system-context.md             (2.3 KB)
│   └── tech-stack.md                 (2.4 KB)
├── 02-domain-model/
│   ├── core-concepts.md
│   ├── data-flow.md
│   └── data-models.md
├── 03-api-interfaces/
│   ├── integration-points.md
│   ├── internal-contracts.md
│   └── public-apis.md
├── 04-critical-paths/
│   ├── error-handling.md
│   ├── main-flows.md
│   └── performance-hotspots.md
├── 05-development-guide/
│   ├── code-conventions.md
│   ├── contribution-guide.md
│   ├── getting-started.md
│   └── testing-strategy.md
└── 06-llm-context/
    ├── codebase.1.txt                (1.5 MB)
    ├── codebase.2.txt                (2.0 MB)
    ├── codebase.3.txt                (2.0 MB)
    ├── codebase.4.txt                (2.0 MB)
    ├── codebase.5.txt                (1.0 MB)
    ├── knowledge-graph-summary.md    (18 KB)
    ├── navigation-guide.md
    ├── pattern-library.md
    ├── prompt-templates.md
    ├── questions-bank.md
    └── semantic-map.json             (6.5 MB)
```

### Executive Summary Output

```markdown
# jito-solana

## At a Glance

> A Rust project

| Attribute      | Value                                                  |
| -------------- | ------------------------------------------------------ |
| **Edition**    | Rust 2021                                              |
| **Crates**     | 142                                                    |
| **Tech Focus** | Serialization (serde), CLI (clap), Parallelism (rayon) |

## Architecture

**Primary Style:** Multi-Crate Workspace (90% confidence)

Multiple crates in a workspace, each with specific responsibility

## Key Decisions

- ✅ **Multi-Crate Workspace** architecture pattern
- ✅ **Hexagonal/Ports-Adapters** architecture pattern
- ✅ **Type-State** design pattern
- ✅ **Error Handling (thiserror)** design pattern
```

### Architecture Styles Detected

| Style                    | Confidence | Description                                |
| ------------------------ | ---------- | ------------------------------------------ |
| Multi-Crate Workspace    | 90%        | Multiple crates in a workspace             |
| Hexagonal/Ports-Adapters | 83%        | Domain logic separated from infrastructure |
| Reactor/Proactor         | 83%        | Async I/O with event loop (Tokio)          |
| Work-Stealing Scheduler  | 75%        | Load-balanced task scheduling              |
| Event-Driven             | 60%        | Components communicate through events      |
| Plugin Architecture      | 50%        | Extensible plugin-based functionality      |

### Design Patterns Detected

| Pattern                    | Confidence | Evidence                               |
| -------------------------- | ---------- | -------------------------------------- |
| Type-State                 | 100%       | `struct Foo<State>`, `impl Foo<State>` |
| Error Handling (thiserror) | 100%       | `#[derive(Error)]`, thiserror import   |
| Error Handling (anyhow)    | 100%       | `.context()`, `anyhow!`, `bail!`       |
| Builder                    | 86%        | `Builder`, `build()`, `with_*` methods |
| Async/Await Runtime        | 50%        | `#[tokio::main]`, `async fn`, `.await` |

### Communication Patterns

| Pattern                   | Usage Count | Evidence            |
| ------------------------- | ----------- | ------------------- |
| Shared State (RwLock)     | 1081        | `Arc<RwLock<...>>`  |
| Shared State (Mutex)      | 306         | `Arc<Mutex<...>>`   |
| Channel-based (tokio)     | 49          | `tokio::sync::mpsc` |
| Channel-based (crossbeam) | 3           | `crossbeam-channel` |

### Knowledge Graph Statistics

| Metric          | Value  |
| --------------- | ------ |
| **Total Nodes** | 15,441 |
| **Total Edges** | 18,930 |
| **Clusters**    | 71     |
| **Functions**   | 12,267 |
| **Structs**     | 2,254  |
| **Enums**       | 607    |
| **Traits**      | 144    |

---

## CLI Reference

### `rust-asr docs`

Generate comprehensive architecture documentation.

```bash
rust-asr docs --path <PROJECT> --output <DIR> [OPTIONS]

Options:
  -p, --path PATH           Path to Rust project (required)
  -o, --output DIR          Output directory (default: project-docs)
  -s, --sections LIST       Comma-separated sections to generate
  --with-ai                 Include AI-enhanced ADRs (requires API key)
  --with-llm-context        Generate 06-llm-context/ section with knowledge graph
  --chunk-size SIZE         Chunk size for repomix (default: 2mb)
```

**Available sections:** `summary`, `architecture`, `domain`, `api`, `paths`, `dev`, `llm-context`

### `rust-asr analyze`

Run full project analysis.

```bash
rust-asr analyze --path ./repos/tokio
rust-asr analyze --repo tokio-rs/tokio --output ./output
```

### `rust-asr patterns`

Detect architectural patterns.

```bash
rust-asr patterns --path ./repos/bevy
```

### `rust-asr deps`

Generate dependency graph.

```bash
rust-asr deps --path ./repos/nushell --format mermaid
rust-asr deps --path ./repos/ripgrep --format dot
rust-asr deps --path ./repos/tokio --format json
```

### `rust-asr architecture`

Extract C4 diagrams and architecture styles.

```bash
rust-asr architecture --path ./repos/zed --output ./analysis
rust-asr architecture --path ./repos/surrealdb --level component
```

### `rust-asr ai-architecture`

AI-enhanced architecture analysis (requires API key).

```bash
rust-asr ai-architecture --path ./repos/ripgrep --output ./ai-output
rust-asr ai-architecture --path ./repos/tokio --adrs-only
rust-asr ai-architecture --path ./repos/bevy --deployment-only
rust-asr ai-architecture --path ./repos/ripgrep --component grep
```

### `rust-asr fetch`

Fetch repositories for analysis.

```bash
rust-asr fetch --champions              # Fetch curated champion projects
rust-asr fetch --count 50               # Fetch top 50 Rust repos
rust-asr fetch --count 10 --metadata-only
```

### `rust-asr compare-patterns`

Compare patterns across champion projects.

```bash
rust-asr compare-patterns --output ./handbook/pattern_comparison.md
```

---

## Champion Projects

Pre-configured projects for architecture study:

| Project         | Crates | Category      | Key Patterns                       |
| --------------- | ------ | ------------- | ---------------------------------- |
| **jito-solana** | 142    | Blockchain    | Type-State, Actor Model, Hexagonal |
| **tokio**       | 10     | Async Runtime | Hexagonal, Work-Stealing           |
| **bevy**        | 83     | Game Engine   | ECS, Plugin Architecture           |
| **zed**         | 224    | Editor        | CRDT, GPUI, Tower Service          |
| **ripgrep**     | 10     | CLI           | Facade, Builder                    |
| **SurrealDB**   | 13     | Database      | Async Runtime                      |
| **nushell**     | 40     | Shell         | Plugin Architecture                |

---

## Data Sources

The `docs` command integrates multiple analysis modules:

| Module                        | Data Extracted                                 | LLM Required  |
| ----------------------------- | ---------------------------------------------- | ------------- |
| `analysis/architecture.py`    | Workspace, C4 diagrams, communication patterns | ❌            |
| `analysis/patterns.py`        | Design patterns (Type-State, Builder, etc.)    | ❌            |
| `analysis/knowledge_graph.py` | Entity relationships, clusters                 | ❌            |
| `export/llm_context.py`       | Codebase chunks via repomix                    | ❌            |
| `ai/ai_architecture.py`       | AI-enhanced ADRs                               | ✅ (optional) |

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ for the Rust community
</p>
