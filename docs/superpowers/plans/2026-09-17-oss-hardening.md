# OSS Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the repository installable, testable, schema-driven, CI-verified, and credible as a small open-source PDF question extraction toolkit.

**Architecture:** Keep deterministic text parsing independent from PDF I/O. Add lightweight typed document construction and validation, then harden the parser and CLI around that contract. Repository-facing documentation, examples, and CI will reflect only implemented behavior.

**Tech Stack:** Python 3.10+, pypdf, pytest, setuptools, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-17-oss-hardening-design.md`

## Global Constraints

- Python floor remains `>=3.10`.
- Keep runtime dependencies minimal; do not add a JSON-schema runtime.
- Do not implement OCR, OpenAI API calls, image/table extraction, formula reconstruction, answer inference, web UI, or database integration in this pass.
- Preserve page-level provenance and raw matched blocks.
- All README capability claims must distinguish implemented features from roadmap items.
- No copyrighted exam PDFs, user documents, secrets, or API keys may be committed.

---

### Task 1: Versioned document model and validation

**Files:**
- Create: `src/exam_pdf_question_extractor/models.py`
- Create: `src/exam_pdf_question_extractor/schema.py`
- Modify: `src/exam_pdf_question_extractor/__init__.py`
- Create: `tests/test_schema.py`

**Interfaces:**
- Produces: `QuestionRecord`, `ExtractionDocument`, `SCHEMA_VERSION`, `ValidationError`, `build_document(source_file: str, questions: list[dict]) -> dict`, `validate_document(document: dict) -> None`.

- [ ] **Step 1: Write failing validation tests** covering valid documents, count mismatch, non-positive question numbers, invalid page values, and non-list options.
- [ ] **Step 2: Run** `pytest tests/test_schema.py -v` and confirm failure because schema/model modules do not exist.
- [ ] **Step 3: Implement typed structures and lightweight validation** using `TypedDict` and explicit checks only.
- [ ] **Step 4: Export public interfaces from `__init__.py`.**
- [ ] **Step 5: Run** `pytest tests/test_schema.py -v` and then `pytest -q`.
- [ ] **Step 6: Commit** with `feat: add versioned extraction schema validation`.

### Task 2: Harden deterministic parser

**Files:**
- Modify: `src/exam_pdf_question_extractor/parser.py`
- Modify: `tests/test_parser.py`

**Interfaces:**
- Consumes: question-record field names defined in Task 1.
- Produces: `extract_questions_from_text(text: str, page: int | None = None) -> list[dict]` supporting ASCII, Arabic-Indic, and Persian digits for question/option labels while remaining conservative.

- [ ] **Step 1: Add failing tests** for multiple questions, Persian digits, numeric labels, multiline text, missing options, and empty/no-question input.
- [ ] **Step 2: Run** `pytest tests/test_parser.py -v` and confirm new cases fail.
- [ ] **Step 3: Implement digit normalization and label matching** without changing the public function signature.
- [ ] **Step 4: Run** parser tests and full suite.
- [ ] **Step 5: Commit** with `feat: support multilingual exam numbering patterns`.

### Task 3: Build validated PDF documents and harden CLI errors

**Files:**
- Modify: `src/exam_pdf_question_extractor/cli.py`
- Create: `tests/test_cli.py`

**Interfaces:**
- Consumes: `build_document()` and `validate_document()` from Task 1; parser from Task 2.
- Produces: `extract_pdf(path: Path) -> dict` returning schema v1 documents and `main() -> int` returning explicit exit codes.

- [ ] **Step 1: Add failing tests** for missing input path, output parent creation, UTF-8 JSON writing helper, and document metadata.
- [ ] **Step 2: Run** `pytest tests/test_cli.py -v` and confirm expected failures.
- [ ] **Step 3: Refactor CLI** so normal user errors print concise stderr messages and return non-zero codes; successful execution returns zero.
- [ ] **Step 4: Keep `if __name__ == "__main__": raise SystemExit(main())`** so console-script behavior receives the code.
- [ ] **Step 5: Run** CLI tests and full suite.
- [ ] **Step 6: Commit** with `feat: validate extraction output and improve cli errors`.

### Task 4: Publish machine-readable schema and reproducible examples

**Files:**
- Create: `schema/question-extraction-v1.schema.json`
- Create: `examples/sample_input.txt`
- Create: `examples/sample_output.json`
- Create: `tests/test_examples.py`

**Interfaces:**
- Consumes: output contract from Task 1.
- Produces: external JSON Schema and examples that match `schema_version = "1.0"`.

- [ ] **Step 1: Add a failing test** loading `examples/sample_output.json` and validating it with the project validator.
- [ ] **Step 2: Run** `pytest tests/test_examples.py -v` and confirm failure because example files do not exist.
- [ ] **Step 3: Add JSON Schema** with required top-level and question fields and exact schema version.
- [ ] **Step 4: Add synthetic, non-copyrighted sample input/output** using a simple FIFO question.
- [ ] **Step 5: Run** example test and full suite.
- [ ] **Step 6: Commit** with `docs: add schema and reproducible examples`.

### Task 5: Add open-source project hygiene

**Files:**
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Create: `CHANGELOG.md`
- Create: `.gitignore`
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/feature_request.yml`

**Interfaces:**
- Produces: contributor setup, security-reporting policy, release history, ignored local artifacts, and structured issue intake.

- [ ] **Step 1: Add contributor instructions** matching the actual `venv`, editable install, and `pytest` commands.
- [ ] **Step 2: Add security policy** stating local-only processing by default and asking reporters not to publish secrets or sensitive documents in public issues.
- [ ] **Step 3: Add changelog entry for `0.1.0`.**
- [ ] **Step 4: Add Python `.gitignore` and concise issue templates.**
- [ ] **Step 5: Verify all referenced commands and paths exist.**
- [ ] **Step 6: Commit** with `docs: add contributor and security project files`.

### Task 6: CI, packaging metadata, and README finalization

**Files:**
- Create: `.github/workflows/ci.yml`
- Modify: `pyproject.toml`
- Modify: `README.md`

**Interfaces:**
- Consumes: completed test suite and examples.
- Produces: GitHub Actions matrix for Python 3.10-3.13, richer package metadata, and accurate public documentation.

- [ ] **Step 1: Add CI workflow** triggered on pushes and pull requests, using `actions/checkout@v4`, `actions/setup-python@v5`, `python -m pip install -e .[dev]`, `pytest -q`, and `exam-pdf-extract --help`.
- [ ] **Step 2: Improve `pyproject.toml` metadata** with project URLs, classifiers, keywords, and pytest test path while keeping dependency footprint unchanged.
- [ ] **Step 3: Rewrite README** with implemented features, limitations, install/CLI/library usage, schema output, examples, development, contribution/security links, and roadmap.
- [ ] **Step 4: Run full tests** and packaging smoke commands in a clean checkout/environment where available.
- [ ] **Step 5: Inspect CI configuration and README for claims not backed by code; remove any such claim.**
- [ ] **Step 6: Commit** with `ci: add test matrix and finalize oss documentation`.

### Task 7: Final verification

**Files:**
- No new files required unless verification reveals a defect.

**Interfaces:**
- Validates all acceptance criteria from the design spec.

- [ ] **Step 1: Run** `pytest -q` and require all tests to pass.
- [ ] **Step 2: Run** `python -m pip install -e .[dev]` in a clean environment where available.
- [ ] **Step 3: Run** `exam-pdf-extract --help` and require exit code 0.
- [ ] **Step 4: Check repository tree** for secrets, accidental PDFs, caches, or unsupported capability claims.
- [ ] **Step 5: Confirm GitHub Actions workflow exists and targets Python 3.10-3.13.**
- [ ] **Step 6: Report only verified capabilities and any remaining limitations.**
