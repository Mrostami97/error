from typing import TypedDict


class QuestionRecord(TypedDict):
    number: int
    text: str
    options: list[str]
    page: int | None
    raw: str


class ExtractionDocument(TypedDict):
    schema_version: str
    source_file: str
    question_count: int
    questions: list[QuestionRecord]
