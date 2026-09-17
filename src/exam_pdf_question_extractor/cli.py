import argparse
import json
from pathlib import Path

from pypdf import PdfReader

from .parser import extract_questions_from_text


def extract_pdf(path: Path) -> dict:
    reader = PdfReader(str(path))
    questions = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        questions.extend(extract_questions_from_text(text, page=page_number))
    return {"source_file": path.name, "questions": questions}


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract exam questions from a text-based PDF into JSON.")
    parser.add_argument("pdf", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, default=Path("questions.json"), help="Output JSON file")
    args = parser.parse_args()

    result = extract_pdf(args.pdf)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Extracted {len(result['questions'])} questions to {args.output}")


if __name__ == "__main__":
    main()
