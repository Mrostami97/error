# Exam PDF Question Extractor

An open-source toolkit for converting exam/question-bank PDFs into structured JSON suitable for search, review, analytics, and downstream educational systems.

## Why this project exists

Large exam archives are difficult to reuse because questions, options, answers, page references, and metadata are locked inside PDFs. This project provides a reproducible extraction pipeline that turns machine-readable PDF text into a normalized JSON structure and keeps source-page provenance for review.

## Current scope

The current MVP focuses on text-based PDFs and extracts:

- numbered questions
- multiple-choice options
- source page numbers
- raw source text for auditability
- deterministic JSON output

OCR, formula reconstruction, image/table extraction, and more advanced layout recovery are planned extensions. The project intentionally does not claim perfect OCR or universal layout support yet.

## Example

```bash
pip install -e .
exam-pdf-extract input.pdf -o questions.json
```

Example output:

```json
{
  "source_file": "input.pdf",
  "questions": [
    {
      "number": 1,
      "text": "Which data structure ...?",
      "options": ["Stack", "Queue", "Tree", "Graph"],
      "page": 3
    }
  ]
}
```

## Design goals

1. Preserve provenance so every extracted item can be checked against its PDF page.
2. Prefer deterministic parsing before model-assisted cleanup.
3. Keep output schema stable and easy to validate.
4. Make the pipeline useful for large public exam archives and educational datasets.

## Development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
pytest
```

## Roadmap

- OCR adapter for scanned PDFs
- formula/LaTeX normalization
- image and table references
- multilingual/Persian exam layout rules
- validation and confidence scoring
- optional model-assisted cleanup with explicit provenance

## License

MIT
