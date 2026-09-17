import argparse
import json
import sys
from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from .parser import extract_questions_from_text
from .schema import ValidationError, build_document, validate_document


def extract_pdf(path: Path) -> dict:
    reader = PdfReader(str(path))
    questions: list[dict] = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        questions.extend(extract_questions_from_text(text, page=page_number))
    return build_document(path.name, questions)


def write_document(document: dict, output: Path) -> None:
    validate_document(document)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract exam questions from a text-based PDF into structured JSON."
    )
    parser.add_argument("pdf", type=Path, help="Input PDF file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("questions.json"),
        help="Output JSON file (default: questions.json)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if not args.pdf.is_file():
        print(f"error: input file not found: {args.pdf}", file=sys.stderr)
        return 2

    try:
        result = extract_pdf(args.pdf)
        write_document(result, args.output)
    except (OSError, PdfReadError, ValidationError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Extracted {result['question_count']} questions to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
