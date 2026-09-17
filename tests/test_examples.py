import json
from pathlib import Path

from exam_pdf_question_extractor import build_document, extract_questions_from_text, validate_document

ROOT = Path(__file__).resolve().parents[1]


def test_sample_output_matches_parser_and_public_contract():
    input_text = (ROOT / "examples" / "sample_input.txt").read_text(encoding="utf-8")
    expected = json.loads((ROOT / "examples" / "sample_output.json").read_text(encoding="utf-8"))
    actual = build_document("sample_input.txt", extract_questions_from_text(input_text))
    validate_document(expected)
    assert actual == expected


def test_json_schema_declares_version_1_contract():
    schema = json.loads((ROOT / "schema" / "question-extraction-v1.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["schema_version"]["const"] == "1.0"
    assert set(schema["required"]) == {"schema_version", "source_file", "question_count", "questions"}
