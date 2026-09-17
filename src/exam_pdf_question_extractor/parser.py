import re
from typing import List, Dict

QUESTION_RE = re.compile(r"(?m)^\s*(\d{1,4})[\).\-:]\s+(.+?)(?=^\s*\d{1,4}[\).\-:]\s+|\Z)", re.S)
OPTION_RE = re.compile(r"(?m)^\s*(?:[A-Da-d]|[1-4]|[۱-۴])[\).\-:]\s+(.+)$")


def extract_questions_from_text(text: str, page: int | None = None) -> List[Dict]:
    """Extract numbered multiple-choice questions from plain text.

    The parser is intentionally deterministic and conservative. It keeps the raw
    question block to make downstream review and debugging easy.
    """
    questions: List[Dict] = []
    for match in QUESTION_RE.finditer(text):
        number = int(match.group(1))
        block = match.group(2).strip()
        options = [m.group(1).strip() for m in OPTION_RE.finditer(block)]

        question_text = block
        first_option = OPTION_RE.search(block)
        if first_option:
            question_text = block[: first_option.start()].strip()

        questions.append(
            {
                "number": number,
                "text": question_text,
                "options": options,
                "page": page,
                "raw": block,
            }
        )
    return questions
