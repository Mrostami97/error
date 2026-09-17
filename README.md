# Exam PDF Question Extractor

[![CI](https://github.com/Mrostami97/exam-pdf-question-extractor/actions/workflows/ci.yml/badge.svg)](https://github.com/Mrostami97/exam-pdf-question-extractor/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A small open-source toolkit for converting **text-based exam and question-bank PDFs** into versioned, auditable JSON.

> **Status:** early alpha. The current implementation intentionally focuses on deterministic text extraction and a stable output contract. OCR and advanced document understanding are roadmap items, not current features.

## What works today

- reads text-based PDFs with `pypdf`;
- extracts numbered question blocks and ordered options;
- recognizes common ASCII, Persian, and Arabic-Indic digit forms;
- preserves one-based source page provenance;
- retains raw matched text for review/debugging;
- emits versioned JSON (`schema_version: "1.0"`);
- validates generated documents before writing them;
- provides a CLI and importable Python API;
- includes automated tests and CI on Python 3.10-3.13.

## What is not implemented yet

- OCR for scanned or image-only PDFs;
- formula/LaTeX reconstruction;
- image or table extraction;
- bounding boxes or page-layout coordinates;
- answer-key inference;
- model-assisted cleanup or OpenAI API integration.

Keeping these limitations explicit is part of the project design: generated data should remain traceable to the source rather than silently guessing structure.

## Installation

```bash
git clone https://github.com/Mrostami97/exam-pdf-question-extractor.git
cd exam-pdf-question-extractor
python -m venv .venv
```

Activate the virtual environment:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install:

```bash
python -m pip install -e .
```

## CLI usage

```bash
exam-pdf-extract input.pdf -o questions.json
```

On success, the CLI prints a concise count and writes UTF-8 JSON. Missing or unreadable inputs return a non-zero exit code with a user-facing error message.

## Python usage

Parse already-extracted text without PDF I/O:

```python
from exam_pdf_question_extractor import build_document, extract_questions_from_text

text = """1. Which structure is FIFO?
A. Stack
B. Queue
C. Tree
D. Graph
"""

questions = extract_questions_from_text(text, page=1)
document = build_document("example.txt", questions)
```

Or read a text-based PDF:

```python
from pathlib import Path
from exam_pdf_question_extractor.cli import extract_pdf

document = extract_pdf(Path("input.pdf"))
```

## Output contract v1

```json
{
  "schema_version": "1.0",
  "source_file": "input.pdf",
  "question_count": 1,
  "questions": [
    {
      "number": 1,
      "text": "Which structure is FIFO?",
      "options": ["Stack", "Queue", "Tree", "Graph"],
      "page": 3,
      "raw": "1. Which structure is FIFO?\nA. Stack\nB. Queue\nC. Tree\nD. Graph"
    }
  ]
}
```

The machine-readable contract is in [`schema/question-extraction-v1.schema.json`](schema/question-extraction-v1.schema.json).

`page` is one-based for PDF extraction and may be `null` when parsing standalone text. `raw` stores the matched source block so downstream cleanup can be audited.

## Parser behavior

The parser is deliberately conservative. It handles common numbered lines using separators such as `.`, `)`, `-`, and `:` and recognizes ASCII (`1`), Persian (`۱`), and Arabic-Indic (`١`) digits. Numeric options using `)` are disambiguated from subsequent question numbers with a deterministic sequence heuristic.

PDF text order still depends on what `pypdf` can recover from the source. Complex multi-column layouts, embedded formulas, and scanned pages may therefore require future adapters.

## Reproducible example

The repository includes synthetic, non-copyrighted fixtures:

- [`examples/sample_input.txt`](examples/sample_input.txt)
- [`examples/sample_output.json`](examples/sample_output.json)

The test suite verifies that parsing the sample input reproduces the checked-in sample output and that the result satisfies the runtime contract.

## Development

```bash
python -m pip install -e ".[dev]"
pytest -q
exam-pdf-extract --help
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines and [SECURITY.md](SECURITY.md) for security reporting.

## Privacy

The current code processes documents locally and makes **no network or API calls**. No document contents are uploaded by this project.

Any future model-assisted functionality must be opt-in and document what data is sent externally.

## Roadmap

Planned directions, subject to tests and review:

- OCR adapter for scanned PDFs;
- richer Persian and multilingual layout rules;
- formula normalization;
- image/table references and layout metadata;
- confidence/validation diagnostics;
- optional model-assisted cleanup with explicit provenance.

## License

MIT. See [LICENSE](LICENSE).
