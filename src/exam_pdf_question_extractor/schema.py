from typing import Any

from .models import ExtractionDocument

SCHEMA_VERSION = "1.0"
_REQUIRED_QUESTION_FIELDS = {"number", "text", "options", "page", "raw"}


class ValidationError(ValueError):
    """Raised when an extraction document violates the public output contract."""


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _validate_question(question: Any, index: int) -> None:
    if not isinstance(question, dict):
        raise ValidationError(f"questions[{index}] must be an object")

    missing = _REQUIRED_QUESTION_FIELDS.difference(question)
    if missing:
        raise ValidationError(
            f"questions[{index}] is missing required fields: {', '.join(sorted(missing))}"
        )

    number = question["number"]
    if not _is_int(number) or number <= 0:
        raise ValidationError(f"questions[{index}].number must be a positive integer")

    if not isinstance(question["text"], str):
        raise ValidationError(f"questions[{index}].text must be a string")

    options = question["options"]
    if not isinstance(options, list) or not all(isinstance(item, str) for item in options):
        raise ValidationError(f"questions[{index}].options must be an array of strings")

    page = question["page"]
    if page is not None and (not _is_int(page) or page <= 0):
        raise ValidationError(f"questions[{index}].page must be null or a positive integer")

    if not isinstance(question["raw"], str):
        raise ValidationError(f"questions[{index}].raw must be a string")


def validate_document(document: Any) -> None:
    if not isinstance(document, dict):
        raise ValidationError("document must be an object")

    if document.get("schema_version") != SCHEMA_VERSION:
        raise ValidationError(f"schema_version must be {SCHEMA_VERSION!r}")

    source_file = document.get("source_file")
    if not isinstance(source_file, str) or not source_file.strip():
        raise ValidationError("source_file must be a non-empty string")

    questions = document.get("questions")
    if not isinstance(questions, list):
        raise ValidationError("questions must be an array")

    count = document.get("question_count")
    if not _is_int(count) or count != len(questions):
        raise ValidationError("question_count must equal the number of questions")

    for index, question in enumerate(questions):
        _validate_question(question, index)


def build_document(source_file: str, questions: list[dict]) -> ExtractionDocument:
    document: ExtractionDocument = {
        "schema_version": SCHEMA_VERSION,
        "source_file": source_file,
        "question_count": len(questions),
        "questions": questions,  # type: ignore[typeddict-item]
    }
    validate_document(document)
    return document
