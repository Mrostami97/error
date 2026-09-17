import re
from typing import Any

_DIGITS = "0-9۰-۹٠-٩"
_NUMBERED_LINE_RE = re.compile(
    rf"^\s*(?P<label>[{_DIGITS}]{{1,4}})\s*(?P<sep>[.)\-:])\s+(?P<text>.+?)\s*$"
)
_ALPHA_OPTION_RE = re.compile(
    r"^\s*(?P<label>[A-Da-d])\s*[.)\-:]\s+(?P<text>.+?)\s*$"
)
_DIGIT_TRANSLATION = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
    "01234567890123456789",
)


def _to_int(label: str) -> int:
    return int(label.translate(_DIGIT_TRANSLATION))


def _normalize(parts: list[str]) -> str:
    return " ".join(part.strip() for part in parts if part.strip())


def extract_questions_from_text(text: str, page: int | None = None) -> list[dict[str, Any]]:
    """Extract numbered exam questions from plain text conservatively.

    The parser recognizes ASCII, Persian, and Arabic-Indic digits. Numeric option
    labels using ``)`` are treated as options while a question is open when they
    follow the expected option sequence. Raw source lines are retained for auditability.
    """
    questions: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    question_parts: list[str] = []
    raw_lines: list[str] = []
    mode = "question"

    def finish_current() -> None:
        nonlocal current, question_parts, raw_lines, mode
        if current is None:
            return
        current["text"] = _normalize(question_parts)
        current["raw"] = "\n".join(raw_lines).strip()
        questions.append(current)
        current = None
        question_parts = []
        raw_lines = []
        mode = "question"

    for original_line in text.splitlines():
        line = original_line.rstrip()
        if not line.strip():
            if current is not None:
                raw_lines.append(line)
            continue

        alpha_option = _ALPHA_OPTION_RE.match(line)
        if current is not None and alpha_option:
            current["options"].append(alpha_option.group("text").strip())
            raw_lines.append(line)
            mode = "option"
            continue

        numbered = _NUMBERED_LINE_RE.match(line)
        if numbered:
            number = _to_int(numbered.group("label"))
            separator = numbered.group("sep")
            content = numbered.group("text").strip()

            numeric_option = (
                current is not None
                and 1 <= number <= 4
                and separator == ")"
                and number == len(current["options"]) + 1
                and number != current["number"] + 1
            )
            if numeric_option:
                current["options"].append(content)
                raw_lines.append(line)
                mode = "option"
                continue

            finish_current()
            current = {
                "number": number,
                "text": "",
                "options": [],
                "page": page,
                "raw": "",
            }
            question_parts = [content]
            raw_lines = [line]
            mode = "question"
            continue

        if current is None:
            continue

        raw_lines.append(line)
        if mode == "option" and current["options"]:
            current["options"][-1] = _normalize([current["options"][-1], line])
        else:
            question_parts.append(line)

    finish_current()
    return questions
