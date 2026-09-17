import pytest

from exam_pdf_question_extractor.schema import (
    SCHEMA_VERSION,
    ValidationError,
    build_document,
    validate_document,
)


def sample_question(**overrides):
    question = {
        "number": 1,
        "text": "Which structure is FIFO?",
        "options": ["Stack", "Queue", "Tree", "Graph"],
        "page": 2,
        "raw": "Which structure is FIFO?\nA. Stack\nB. Queue\nC. Tree\nD. Graph",
    }
    question.update(overrides)
    return question


def test_build_document_sets_version_and_count():
    doc = build_document("exam.pdf", [sample_question()])
    assert doc["schema_version"] == SCHEMA_VERSION == "1.0"
    assert doc["source_file"] == "exam.pdf"
    assert doc["question_count"] == 1


def test_validate_rejects_count_mismatch():
    doc = build_document("exam.pdf", [sample_question()])
    doc["question_count"] = 2
    with pytest.raises(ValidationError, match="question_count"):
        validate_document(doc)


@pytest.mark.parametrize("number", [0, -1, True])
def test_validate_rejects_non_positive_question_numbers(number):
    with pytest.raises(ValidationError, match="number"):
        build_document("exam.pdf", [sample_question(number=number)])


@pytest.mark.parametrize("page", [0, -2, False])
def test_validate_rejects_invalid_page_values(page):
    with pytest.raises(ValidationError, match="page"):
        build_document("exam.pdf", [sample_question(page=page)])


def test_validate_allows_null_page_for_raw_text_parsing():
    doc = build_document("inline.txt", [sample_question(page=None)])
    validate_document(doc)


def test_validate_rejects_non_list_options():
    with pytest.raises(ValidationError, match="options"):
        build_document("exam.pdf", [sample_question(options="Queue")])
