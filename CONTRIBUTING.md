# Contributing

Thanks for helping improve Exam PDF Question Extractor.

## Development setup

Requirements: Python 3.10+ and Git.

```bash
git clone https://github.com/Mrostami97/exam-pdf-question-extractor.git
cd exam-pdf-question-extractor
python -m venv .venv
```

Activate the environment, then install development dependencies:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install -e ".[dev]"
```

Run the checks:

```bash
pytest -q
exam-pdf-extract --help
```

## Project principles

- Keep deterministic parsing separate from PDF I/O.
- Preserve source provenance (`page` and `raw`) for auditability.
- Prefer a conservative parser over silently inventing structure.
- Keep runtime dependencies small.
- Do not claim support for OCR, formulas, images, tables, or model-assisted cleanup until those features are implemented and tested.

## Reporting extraction problems

When possible, create a minimal synthetic text sample and include the input, actual result, expected result, and Python version.

Please do not upload copyrighted exam PDFs, API keys, private documents, or sensitive personal data to public issues.

## Pull requests

Before opening a pull request, add or update tests for behavior changes, run `pytest -q`, smoke-test the CLI, and update README/schema examples when the public output contract changes.
