# Konkur Integration Design

## Goal

Add an optional export path from `exam-pdf-question-extractor` to the existing `Mrostami97/konkur` ingestion contract without changing the Konkur application architecture, database schema, API module boundaries, deployment stack, or review/publish workflow.

## Architectural principle

The extractor remains an independent OSS tool. `konkur` remains the owner of its canonical `question.v1` contract and its existing ZIP ingestion workflow. The integration is an adapter at the boundary: extractor output is transformed into the exact package shape that `konkur` already accepts.

No runtime dependency, Git submodule, package dependency, database coupling, or cross-repository import is introduced.

## Existing Konkur contract

The target system already accepts a ZIP archive with `payload.json` at the root. `payload.json` may contain `{ "items": [...] }`; each question item uses `schema_version: "question.v1"`.

A valid question requires:

- `schema_version`
- `external_id`
- `exam.degree`, `exam.major`, `exam.year`
- `subject_code`
- at least one `topic_codes` entry
- at least one `stem_blocks` entry
- exactly four options numbered 1 through 4
- `correct_option` in 1 through 4
- at least one `solution_blocks` entry
- `provenance.producer_type`
- `provenance.source_artifact`

The integration must not weaken or bypass these requirements.

## Proposed extractor interface

Add a new optional export command/profile named `konkur` that converts an already-extracted document into a `question.v1` import package.

The first implementation will support text-only questions. It will not invent LaTeX, images, tables, answer keys, subjects, topics, solutions, or exam metadata.

Required user-supplied metadata for an import-ready package:

- degree: `master` or `phd`
- major: non-empty string
- year: integer in the valid Konkur range
- subject code: non-empty string
- at least one topic code
- one correct answer per exported question
- one non-empty solution per exported question

The source PDF filename and page/question provenance from extraction are preserved where possible.

## Safety and correctness rules

1. Never fabricate a correct option.
2. Never fabricate a solution.
3. Never silently choose subject/topic metadata.
4. Never emit a package if any question lacks exactly four options.
5. Never bypass Konkur's existing review workflow.
6. Never write directly to the Konkur database.
7. Never change Prisma schemas, migrations, API controllers/services, web application code, Docker configuration, or deployment code as part of this integration.
8. All generated `external_id` values must be deterministic for the same source/metadata/question number.
9. Generated JSON must use UTF-8 and preserve Persian text.
10. Generated package content must validate against the semantics of `question.v1` before the ZIP is written.

## Data mapping

Extractor question -> Konkur question:

- extracted question text -> `stem_blocks: [{ "type": "text", "text": ... }]`
- four extracted option strings -> `options[].blocks` text blocks
- extracted page -> `source.page`
- extracted number -> `source.question_number`
- source filename -> `provenance.source_artifact`
- producer -> `producer_type: "external_ai"` only when the package is produced through this extraction tool; `producer_name` identifies `exam-pdf-question-extractor`
- CLI metadata -> `exam`, `subject_code`, `topic_codes`
- supplied answer key -> `correct_option`
- supplied solution text -> `solution_blocks`

## Input shape for answers and solutions

To keep the CLI reproducible and avoid a large argument surface, import-specific answers and solutions will be supplied through a JSON metadata file.

Example:

```json
{
  "degree": "master",
  "major": "computer-engineering",
  "year": 1405,
  "subject_code": "data-structures",
  "topic_codes": ["graphs"],
  "answers": {
    "1": 2,
    "2": 4
  },
  "solutions": {
    "1": "Queue is FIFO.",
    "2": "..."
  }
}
```

Question keys refer to the extracted question number.

## CLI behavior

A dedicated command will package an extracted JSON document:

```bash
exam-pdf-extract-konkur questions.json \
  --metadata konkur-metadata.json \
  -o konkur-import.zip
```

The command will:

1. read and validate the extractor document;
2. read and validate integration metadata;
3. convert every question to `question.v1`;
4. reject incomplete or ambiguous items with actionable errors;
5. write `payload.json` into a ZIP archive;
6. make no network calls and perform no automatic upload.

Keeping upload out of the extractor preserves the existing authenticated admin boundary in `konkur`.

## Konkur repository changes

The `konkur` repository receives documentation only:

- `docs/integrations/exam-pdf-question-extractor.md`
- optionally one short README link to that document

The documentation explains that the external OSS extractor can generate a package accepted by the existing `/admin/import` workflow. No production source files are modified.

## Testing

Extractor tests will cover:

- successful conversion of a four-option Persian/English question;
- deterministic `external_id` generation;
- missing answer failure;
- invalid answer range failure;
- missing solution failure;
- wrong option count failure;
- missing topic/subject/exam metadata failure;
- UTF-8 preservation in `payload.json`;
- ZIP contains exactly the expected root `payload.json` for text-only imports;
- payload values match Konkur `question.v1` field names and required semantics.

Existing extractor tests must continue to pass.

For `konkur`, the integration change is documentation-only, so existing application code and CI behavior remain unchanged.

## Out of scope

- automatic API upload to Konkur
- database writes
- OCR changes
- automatic answer generation
- automatic solution generation
- automatic subject/topic classification
- image/table/LaTeX asset packaging
- changes to Konkur's `question.v1` schema
- changes to Konkur review/publish behavior

These can be designed separately after the text-only adapter is stable.
