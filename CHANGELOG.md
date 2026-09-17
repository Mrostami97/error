# Changelog

All notable changes to this project are documented here.

## [0.1.0] - 2026-09-17

### Added

- deterministic extraction of numbered questions and multiple-choice options from text-based PDFs;
- support for ASCII, Persian, and Arabic-Indic digits in common numbered layouts;
- page-level provenance and raw matched text;
- versioned JSON output contract (`1.0`) with lightweight runtime validation;
- machine-readable JSON Schema and reproducible synthetic examples;
- command-line interface with explicit user-facing errors;
- automated tests and GitHub Actions CI;
- contribution and security documentation.

### Limitations

- no OCR for scanned/image-only PDFs;
- no formula, image, table, or layout-coordinate reconstruction;
- no answer-key inference;
- no external model or API integration.
