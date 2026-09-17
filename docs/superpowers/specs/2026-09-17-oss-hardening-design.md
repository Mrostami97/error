# OSS Hardening Design

Date: 2026-09-17
Status: Approved direction, implementation pending

## Goal

Turn the current MVP into a small but credible open-source project that a reviewer can understand, install, run, test, and extend. The project must remain honest about its current capabilities: deterministic extraction from text-based PDFs is implemented; OCR, formula reconstruction, image/table recovery, and model-assisted cleanup remain roadmap items until implemented.

## Principles

1. Keep the extraction core deterministic and auditable.
2. Preserve source provenance for every extracted question.
3. Define a stable, documented JSON contract before adding advanced extraction features.
4. Prefer tests and reproducible examples over broad capability claims.
5. Keep the dependency footprint small.
6. Make CI validate the exact installation and test workflow documented in the README.

## Architecture

The package remains a small Python library with four clear responsibilities:

- `parser.py`: deterministic parsing of normalized page text into question records.
- `cli.py`: PDF reading, page iteration, output serialization, and user-facing exit behavior.
- `schema.py`: versioned output-contract helpers and lightweight validation for produced JSON.
- `models.py`: typed structures for questions and extraction documents, without introducing a heavy validation framework.

The CLI reads a text-based PDF through `pypdf`, passes each page's extracted text to the deterministic parser, constructs a versioned extraction document, validates it, and writes UTF-8 JSON. Parsing remains usable independently of PDF I/O for testing and downstream integrations.

## Output Contract v1

Top-level document:

- `schema_version`: string, initially `1.0`.
- `source_file`: source PDF filename.
- `question_count`: integer equal to the number of question objects.
- `questions`: array of question objects.

Question object:

- `number`: positive integer when a number is detected.
- `text`: normalized question text.
- `options`: ordered array of option strings.
- `page`: one-based source PDF page number, or null when parsing raw text directly.
- `raw`: original matched question block used for audit/debugging.

The first version intentionally does not claim correct-answer extraction, confidence scores, OCR metadata, image coordinates, or formula reconstruction.

## Parser Improvements

The parser should support the currently documented English pattern plus common Persian/Arabic digits and common question/option separators. It should remain conservative: ambiguous blocks should not be silently invented as valid four-option questions.

Tests will cover:

- multiple questions on one page;
- English option labels;
- numeric option labels;
- Persian digits;
- page provenance;
- missing options;
- multiline question text;
- no-question input.

## CLI Behavior

The CLI will:

- fail clearly when the input path does not exist or is not a file;
- produce UTF-8 JSON with non-ASCII characters preserved;
- create parent directories for the requested output path when reasonable;
- return a non-zero exit code for unreadable/invalid PDFs;
- print a concise success summary including extracted question count.

## Validation

A lightweight validator will check invariants of generated documents, including schema version, question count consistency, required fields, positive question numbers, valid page values, and option-array shape. Validation errors should be explicit and suitable for tests.

No third-party JSON-schema runtime is required in the MVP. A machine-readable `schema/question-extraction-v1.schema.json` file will also be included for external consumers.

## Repository Quality

Add the following project-facing files:

- `CONTRIBUTING.md` with local setup, tests, coding expectations, and issue guidance;
- `SECURITY.md` with a simple private-reporting policy and scope statement;
- `CHANGELOG.md` starting at `0.1.0`;
- `.gitignore` for Python development artifacts;
- `.github/workflows/ci.yml` running install and tests on supported Python versions;
- issue templates for bug reports and feature requests;
- `examples/sample_input.txt` and `examples/sample_output.json` demonstrating the contract without committing copyrighted exam material.

## README Structure

The README will be revised to include:

1. concise project purpose;
2. implemented capabilities vs roadmap;
3. installation;
4. CLI usage;
5. library usage;
6. documented JSON output;
7. reproducible example;
8. development/test commands;
9. contribution and security links;
10. limitations;
11. roadmap;
12. MIT license.

Claims about OCR, AI cleanup, formulas, images, tables, or Persian-layout intelligence will be clearly labeled as planned work unless code for them exists.

## CI and Quality Gates

GitHub Actions will run on pushes and pull requests. The initial matrix will target Python 3.10, 3.11, 3.12, and 3.13. Each job will:

1. check out the repository;
2. install the package with development dependencies;
3. run `pytest`;
4. invoke the CLI help command as a packaging smoke test.

The implementation will avoid adding lint/format tools solely for appearance; those can be introduced later when they provide real maintenance value.

## Error Handling

Parser functions should return an empty list when no supported questions are found. Structural validation errors raise a dedicated validation exception. CLI-facing file/PDF errors are converted to concise stderr messages and non-zero exits rather than raw tracebacks during normal user errors.

## Security and Privacy

The project processes local documents and should not upload document contents by default. Any future model-assisted feature must be opt-in and document exactly what data is sent to an external API. No API keys, user documents, or proprietary exam archives will be committed to the repository.

## Non-goals for this hardening pass

- OCR implementation;
- OpenAI API integration;
- image/table extraction;
- formula/LaTeX reconstruction;
- answer-key inference;
- web UI;
- database integration;
- benchmark claims without a published benchmark dataset.

These are intentionally deferred so the repository remains credible and testable.

## Acceptance Criteria

The hardening pass is complete when:

- a fresh Python environment can install the package from the repository;
- all automated tests pass locally and in GitHub Actions;
- the CLI produces a document conforming to output contract v1;
- examples match the documented schema;
- README statements distinguish implemented features from roadmap work;
- contribution, security, and change history documentation are present;
- no secrets or copyrighted source PDFs are included.
