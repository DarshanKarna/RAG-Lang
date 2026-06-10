# Error Explanation & Fix

## The Error

```
pymupdf.FileNotFoundError: no such file: './my_documents/sample.pdf.pdf'
```

PyMuPDF (`fitz.open()`) tried to open the file at path `./my_documents/sample.pdf.pdf`
but no such file exists on disk.

## Root Cause — TWO typos in `test.rag` line 1

The current line reads:

```
LOAD "./my_documents/sample.pdf.pdf"
```

There are **two separate mistakes** here:

### 1. Wrong folder name: `my_documents` → should be `my-documents`

The actual folder in the project is named **`my-documents`** (with a **hyphen** `-`),
but the `.rag` script uses **`my_documents`** (with an **underscore** `_`).

These are two completely different paths to the operating system.

### 2. Duplicate file extension: `sample.pdf.pdf` → should be `sample.pdf`

The file in `my-documents/` is called **`sample.pdf`**, but the script references
**`sample.pdf.pdf`** — the `.pdf` extension was accidentally typed twice.

## The Fix

Change line 1 of `test.rag` from:

```diff
- LOAD "./my_documents/sample.pdf.pdf"
+ LOAD "./my-documents/sample.pdf"
```

This corrects both issues:
- `my_documents` → `my-documents`  (underscore → hyphen)
- `sample.pdf.pdf` → `sample.pdf`  (remove duplicate extension)

No changes are needed in `engine.py`, `parser.py`, or `grammar.lark` — the bug is
entirely in the `.rag` script's file path string.
