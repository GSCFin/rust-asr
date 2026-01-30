<p align="center">
  <img src="https://img.shields.io/badge/Rust-Khôi%20Phục%20Kiến%20Trúc-orange?style=for-the-badge&logo=rust" alt="Rust ASR">
</p>

<h1 align="center">🦀 Rust ASR</h1>

<p align="center">
  <strong>Bộ Công Cụ Khôi Phục Kiến Trúc Phần Mềm cho Dự Án Rust</strong>
</p>

<p align="center">
  <a href="#tính-năng">Tính năng</a> •
  <a href="#cài-đặt">Cài đặt</a> •
  <a href="#bắt-đầu-nhanh">Bắt đầu nhanh</a> •
  <a href="#ví-dụ-đầu-ra">Ví dụ đầu ra</a> •
  <a href="#tham-khảo-cli">Tham khảo CLI</a> •
  <a href="#giấy-phép">Giấy phép</a>
</p>

<p align="center">
  <a href="README.md">🇬🇧 English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="Giấy phép: MIT">
  <img src="https://img.shields.io/badge/AI-Gemini%20Powered-purple.svg" alt="AI Powered">
</p>

> [!WARNING]
> **🚧 Trạng Thái Dự Án: Đang Phát Triển**
>
> Dự án này vẫn đang trong giai đoạn phát triển ban đầu. Nhiều công cụ và module phân tích cần được tinh chỉnh thêm. Chúng tôi hoan nghênh mọi đóng góp và phản hồi!

---

Bộ công cụ Python toàn diện để trích xuất kiến thức kiến trúc từ các dự án Rust. Tạo **tài liệu sẵn sàng cho PM**, **sơ đồ C4**, **đồ thị tri thức**, và **ngữ cảnh tối ưu cho LLM** — tất cả từ phân tích tĩnh mà không cần chạy chương trình.

## Tính năng

### 📊 Phân Tích Tĩnh (Không cần LLM)

| Tính năng                | Mô tả                                                       |
| ------------------------ | ----------------------------------------------------------- |
| **Đồ thị Phụ thuộc**     | Phân tích phụ thuộc crate, xác định các thành phần cốt lõi  |
| **Cấu trúc Module**      | Ánh xạ ranh giới khả kiến (`pub` vs `pub(crate)`)           |
| **Nhận dạng Pattern**    | Phát hiện Tower Service, ECS, Type-State, Builder patterns  |
| **Phong cách Kiến trúc** | Hexagonal, Actor Model, Plugin, Multi-Crate Workspace       |
| **Pattern Giao tiếp**    | Channel-based, Shared State (Mutex/RwLock), Message Passing |

### 🤖 Phân Tích Nâng Cao với AI (Gemini)

| Tính năng              | Mô tả                                           |
| ---------------------- | ----------------------------------------------- |
| **Sơ đồ C4**           | Tự động tạo sơ đồ Context, Container, Component |
| **Trích xuất ADR**     | Suy luận Architectural Decision Records từ code |
| **Mô hình Triển khai** | Phân tích yêu cầu runtime và pattern mở rộng    |

### 📚 Xuất Tài Liệu (Cấu trúc 5+1)

Tạo **18+ file** trong 6 phần:

```
output/
├── 00-executive-summary.md      # Tổng quan, tech stack, quyết định chính
├── 01-architecture/             # Sơ đồ C4, styles, ADRs
├── 02-domain-model/             # Thực thể, kiểu dữ liệu, luồng dữ liệu
├── 03-api-interfaces/           # API công khai, contracts
├── 04-critical-paths/           # Luồng chính, xử lý lỗi
├── 05-development-guide/        # Hướng dẫn bắt đầu, quy ước
└── 06-llm-context/              # Đồ thị tri thức, các phần codebase
```

### 🧠 Tạo Ngữ Cảnh LLM

Cho phát triển hỗ trợ AI và hiểu kiến trúc:

| Đầu ra                | Mô tả                                           |
| --------------------- | ----------------------------------------------- |
| **Codebase Chunks**   | Chia codebase thành các phần ~2MB qua repomix   |
| **Đồ thị Tri thức**   | Quan hệ thực thể với 15K+ nodes                 |
| **Chỉ mục Ngữ nghĩa** | Hướng dẫn điều hướng để khám phá codebase       |
| **Thư viện Pattern**  | Các design patterns được tài liệu hóa với ví dụ |
| **Mẫu Prompt**        | Các prompt sẵn dùng cho câu hỏi kiến trúc       |

---

## Cài đặt

### Yêu cầu

- Python 3.10+
- [repomix](https://github.com/yamadashy/repomix) (cho tạo ngữ cảnh LLM)

### Cài đặt từ source

```bash
# Clone repository
git clone https://github.com/your-org/rust-asr.git
cd rust-asr

# Cài đặt với pip (chế độ editable)
pip install -e .

# Cho tính năng AI (tùy chọn)
pip install -e ".[ai]"
```

### Cấu hình AI (Tùy chọn)

```bash
cp .env.example .env
# Chỉnh sửa .env với GOOGLE_API_KEY của bạn
```

**Ví dụ .env:**

```bash
GOOGLE_API_KEY=your_api_key_here
GOOGLE_API_URL=https://generativelanguage.googleapis.com/v1beta/openai
GOOGLE_MODEL=gemini-2.0-flash
```

---

## Bắt Đầu Nhanh

### Tải Các Dự Án Mẫu

```bash
# Tải các dự án Rust được chọn lọc để phân tích
rust-asr fetch --champions
```

### Tạo Tài Liệu Đầy Đủ

```bash
# Tài liệu cơ bản (18 files, 0 yêu cầu LLM)
rust-asr docs --path ./repos/tokio --output ./output/tokio

# Với phần ngữ cảnh LLM (đồ thị tri thức, codebase chunks)
rust-asr docs --path ./repos/jito-solana --output ./output/jito-solana --with-llm-context

# Với ADRs nâng cao bằng AI
rust-asr docs --path ./repos/bevy --output ./output/bevy --with-ai
```

### Phát Hiện Pattern

```bash
rust-asr patterns --path ./repos/zed
```

### Phân Tích Kiến Trúc

```bash
rust-asr architecture --path ./repos/ripgrep --output ./analysis
```

---

## Ví Dụ Đầu Ra

### Case Study: jito-solana (Fork Blockchain Solana)

Chạy phân tích "cold" đầy đủ trên codebase jito-solana:

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

### Cấu Trúc Được Tạo

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

### Phong Cách Kiến Trúc Phát Hiện Được

| Phong cách               | Độ tin cậy | Mô tả                                      |
| ------------------------ | ---------- | ------------------------------------------ |
| Multi-Crate Workspace    | 90%        | Nhiều crates trong một workspace           |
| Hexagonal/Ports-Adapters | 83%        | Logic domain tách biệt khỏi infrastructure |
| Reactor/Proactor         | 83%        | Async I/O với event loop (Tokio)           |
| Work-Stealing Scheduler  | 75%        | Lập lịch task cân bằng tải                 |
| Event-Driven             | 60%        | Các thành phần giao tiếp qua events        |
| Plugin Architecture      | 50%        | Chức năng mở rộng dựa trên plugin          |

### Design Patterns Phát Hiện Được

| Pattern                    | Độ tin cậy | Bằng chứng                                |
| -------------------------- | ---------- | ----------------------------------------- |
| Type-State                 | 100%       | `struct Foo<State>`, `impl Foo<State>`    |
| Error Handling (thiserror) | 100%       | `#[derive(Error)]`, thiserror import      |
| Error Handling (anyhow)    | 100%       | `.context()`, `anyhow!`, `bail!`          |
| Builder                    | 86%        | `Builder`, `build()`, các method `with_*` |
| Async/Await Runtime        | 50%        | `#[tokio::main]`, `async fn`, `.await`    |

### Thống Kê Đồ Thị Tri Thức

| Chỉ số         | Giá trị |
| -------------- | ------- |
| **Tổng Nodes** | 15,441  |
| **Tổng Edges** | 18,930  |
| **Clusters**   | 71      |
| **Functions**  | 12,267  |
| **Structs**    | 2,254   |
| **Enums**      | 607     |
| **Traits**     | 144     |

---

## Tham Khảo CLI

### `rust-asr docs`

Tạo tài liệu kiến trúc toàn diện.

```bash
rust-asr docs --path <PROJECT> --output <DIR> [OPTIONS]

Tùy chọn:
  -p, --path PATH           Đường dẫn đến dự án Rust (bắt buộc)
  -o, --output DIR          Thư mục đầu ra (mặc định: project-docs)
  -s, --sections LIST       Danh sách các phần cách nhau bởi dấu phẩy
  --with-ai                 Bao gồm ADRs nâng cao bằng AI (cần API key)
  --with-llm-context        Tạo phần 06-llm-context/ với đồ thị tri thức
  --chunk-size SIZE         Kích thước chunk cho repomix (mặc định: 2mb)
```

**Các phần có sẵn:** `summary`, `architecture`, `domain`, `api`, `paths`, `dev`, `llm-context`

### `rust-asr analyze`

Chạy phân tích dự án đầy đủ.

```bash
rust-asr analyze --path ./repos/tokio
rust-asr analyze --repo tokio-rs/tokio --output ./output
```

### `rust-asr patterns`

Phát hiện các pattern kiến trúc.

```bash
rust-asr patterns --path ./repos/bevy
```

### `rust-asr deps`

Tạo đồ thị phụ thuộc.

```bash
rust-asr deps --path ./repos/nushell --format mermaid
rust-asr deps --path ./repos/ripgrep --format dot
rust-asr deps --path ./repos/tokio --format json
```

### `rust-asr architecture`

Trích xuất sơ đồ C4 và phong cách kiến trúc.

```bash
rust-asr architecture --path ./repos/zed --output ./analysis
rust-asr architecture --path ./repos/surrealdb --level component
```

### `rust-asr ai-architecture`

Phân tích kiến trúc nâng cao bằng AI (cần API key).

```bash
rust-asr ai-architecture --path ./repos/ripgrep --output ./ai-output
rust-asr ai-architecture --path ./repos/tokio --adrs-only
rust-asr ai-architecture --path ./repos/bevy --deployment-only
rust-asr ai-architecture --path ./repos/ripgrep --component grep
```

### `rust-asr fetch`

Tải repositories để phân tích.

```bash
rust-asr fetch --champions              # Tải các dự án mẫu được chọn lọc
rust-asr fetch --count 50               # Tải top 50 Rust repos
rust-asr fetch --count 10 --metadata-only
```

---

## Các Dự Án Mẫu

Các dự án được cấu hình sẵn để nghiên cứu kiến trúc:

| Dự án           | Crates | Thể loại      | Patterns chính                     |
| --------------- | ------ | ------------- | ---------------------------------- |
| **jito-solana** | 142    | Blockchain    | Type-State, Actor Model, Hexagonal |
| **tokio**       | 10     | Async Runtime | Hexagonal, Work-Stealing           |
| **bevy**        | 83     | Game Engine   | ECS, Plugin Architecture           |
| **zed**         | 224    | Editor        | CRDT, GPUI, Tower Service          |
| **ripgrep**     | 10     | CLI           | Facade, Builder                    |
| **SurrealDB**   | 13     | Database      | Async Runtime                      |
| **nushell**     | 40     | Shell         | Plugin Architecture                |

---

## Đóng Góp

Chúng tôi hoan nghênh mọi đóng góp! Vui lòng gửi Pull Request.

1. Fork repository
2. Tạo nhánh tính năng (`git checkout -b feature/amazing-feature`)
3. Commit thay đổi (`git commit -m 'Thêm tính năng tuyệt vời'`)
4. Push nhánh (`git push origin feature/amazing-feature`)
5. Mở Pull Request

---

## Giấy Phép

Dự án này được cấp phép theo Giấy phép MIT - xem file [LICENSE](LICENSE) để biết chi tiết.

---

<p align="center">
  Made with ❤️ cho cộng đồng Rust
</p>
