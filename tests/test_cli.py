import json

import exam_pdf_question_extractor.cli as cli
from exam_pdf_question_extractor.schema import build_document


class FakePage:
    def __init__(self, text: str):
        self._text = text

    def extract_text(self):
        return self._text


class FakeReader:
    def __init__(self, _path: str):
        self.pages = [
            FakePage("1. Which structure is FIFO?\nA. Stack\nB. Queue\n"),
            FakePage("2. Which structure is LIFO?\nA. Stack\nB. Queue\n"),
        ]


def test_extract_pdf_returns_versioned_document(monkeypatch, tmp_path):
    pdf = tmp_path / "exam.pdf"
    pdf.write_bytes(b"fake")
    monkeypatch.setattr(cli, "PdfReader", FakeReader)
    result = cli.extract_pdf(pdf)
    assert result["schema_version"] == "1.0"
    assert result["source_file"] == "exam.pdf"
    assert result["question_count"] == 2
    assert [q["page"] for q in result["questions"]] == [1, 2]


def test_write_document_creates_parent_and_preserves_unicode(tmp_path):
    document = build_document("exam.pdf", [{
        "number": 1,
        "text": "کدام گزینه درست است؟",
        "options": ["اول", "دوم"],
        "page": 1,
        "raw": "کدام گزینه درست است؟",
    }])
    output = tmp_path / "nested" / "questions.json"
    cli.write_document(document, output)
    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded["questions"][0]["text"] == "کدام گزینه درست است؟"


def test_main_returns_nonzero_for_missing_input(tmp_path, capsys):
    code = cli.main([str(tmp_path / "missing.pdf")])
    captured = capsys.readouterr()
    assert code != 0
    assert "not found" in captured.err.lower()


def test_main_writes_output_and_returns_zero(monkeypatch, tmp_path, capsys):
    pdf = tmp_path / "exam.pdf"
    pdf.write_bytes(b"fake")
    output = tmp_path / "out" / "questions.json"
    document = build_document("exam.pdf", [])
    monkeypatch.setattr(cli, "extract_pdf", lambda _path: document)
    code = cli.main([str(pdf), "-o", str(output)])
    assert code == 0
    assert output.exists()
    assert "Extracted 0 questions" in capsys.readouterr().out
