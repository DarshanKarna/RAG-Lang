# RAG-Lang

A declarative Domain-Specific Language (DSL) for orchestrating Retrieval-Augmented Generation pipelines — write simple, English-like scripts instead of boilerplate Python code.

## What is RAG-Lang?

RAG-Lang bridges **compiler theory** and **generative AI**. It provides a minimal, purpose-built language that lets you describe an entire RAG workflow in a few lines:

```text
LOAD "./my-documents/sample.pdf"
CHUNK 500 OVERLAP 50
AGENT "Support_Bot" MODEL "gpt-4o"
QUERY "Can you summarize the main points of this document?"
```

The RAG-Lang compiler parses this script into a structured Abstract Syntax Tree (AST), then executes each instruction against a real backend — extracting text from PDFs, splitting it into chunks, configuring an LLM agent, and assembling the final prompt payload.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  .rag Script │────▶│  Lark Parser  │────▶│  Transformer  │────▶│   Engine      │
│  (DSL Source)│     │  (LALR(1))    │     │  (AST Builder) │     │  (Interpreter)│
└─────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                           │                                          │
                     grammar.lark                              PyMuPDF · LangChain
```

| Layer | File | Role |
|-------|------|------|
| **Grammar** | `grammar.lark` | EBNF rules defining the DSL syntax |
| **Parser** | `parser.py` | Lark `Transformer` that converts tokens → Python dicts (AST) |
| **Engine** | `engine.py` | Interpreter that walks the AST and executes each pipeline step |
| **Script** | `test.rag` | Example user-authored RAG pipeline |

## DSL Commands

| Command | Syntax | Description |
|---------|--------|-------------|
| `LOAD`  | `LOAD "<path>"` | Extract text from a PDF file using PyMuPDF |
| `CHUNK` | `CHUNK <size> OVERLAP <overlap>` | Split extracted text into chunks using LangChain's `RecursiveCharacterTextSplitter` |
| `AGENT` | `AGENT "<name>" MODEL "<model>"` | Configure a named LLM agent with a specific model |
| `QUERY` | `QUERY "<question>"` | Run a query against the chunked documents through the configured agent |

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/DarshanKarna/RAG-Lang.git
cd RAG-Lang

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install lark PyMuPDF langchain-text-splitters langchain-core
```

### Running

```bash
python engine.py
```

This executes the `test.rag` script, which:
1. Loads and extracts text from `./my-documents/sample.pdf`
2. Splits the text into 500-character chunks with 50-character overlap
3. Configures a `Support_Bot` agent targeting `gpt-4o`
4. Merges the retrieved chunks with the query into a formatted LLM payload

## Project Structure

```
RAG-Lang/
├── grammar.lark          # DSL grammar definition (EBNF)
├── parser.py             # Lark Transformer (tokens → AST)
├── engine.py             # Runtime interpreter and pipeline executor
├── test.rag              # Example RAG pipeline script
├── my-documents/
│   └── sample.pdf        # Sample PDF for testing
├── error_explanation.md   # Documented bug fix reference
├── .gitignore
└── README.md
```

## How It Works

**1. Parse** — Lark reads `grammar.lark` and tokenizes the `.rag` script using an LALR(1) parser.

**2. Transform** — The `RAGTransformer` converts raw tokens into a list of Python dictionaries (the AST):

```python
[
    {"action": "load_documents", "path": "./my-documents/sample.pdf"},
    {"action": "configure_chunking", "chunk_size": 500, "overlap": 50},
    {"action": "initialize_agent", "agent_name": "Support_Bot", "model_type": "gpt-4o"},
    {"action": "run_query", "question": "Can you summarize the main points of this document?"}
]
```

**3. Execute** — The engine walks the AST sequentially, routing each instruction to the appropriate function (`fitz.open`, `RecursiveCharacterTextSplitter`, `ChatPromptTemplate`, etc.).

## Technical Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Language Parsing | [Lark](https://github.com/lark-parser/lark) | LALR(1) grammar parsing and tree transformation |
| PDF Ingestion | [PyMuPDF](https://github.com/pymupdf/PyMuPDF) | High-fidelity text extraction from PDF documents |
| Text Processing | [LangChain Text Splitters](https://github.com/langchain-ai/langchain) | Recursive chunk allocation with configurable overlap |
| Prompt Engineering | [LangChain Core](https://github.com/langchain-ai/langchain) | `ChatPromptTemplate` for structured LLM payloads |

## Development Roadmap

- [x] Environment setup and project scaffolding
- [x] Grammar definition — `LOAD`, `CHUNK`, `AGENT` commands
- [x] Parser and Transformer construction
- [x] Engine integration with sequential AST execution
- [x] PDF text ingestion via PyMuPDF
- [x] Text chunking via LangChain `RecursiveCharacterTextSplitter`
- [x] LLM agent configuration via `ChatPromptTemplate`
- [x] `QUERY` command — RAG context merging and LLM payload formatting
- [ ] Live LLM API call execution (OpenAI / Gemini)
- [ ] Vector store integration for semantic retrieval
- [ ] Multi-document support
- [ ] Error handling and DSL diagnostics

## License

This project is open source and available for academic and personal use.

---

Developed by **Darshan Karna**
