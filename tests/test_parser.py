from exam_pdf_question_extractor import extract_questions_from_text


def test_extracts_question_and_options():
    text = """1. Which structure is FIFO?
A. Stack
B. Queue
C. Tree
D. Graph
"""
    questions = extract_questions_from_text(text, page=2)
    assert len(questions) == 1
    assert questions[0]["number"] == 1
    assert questions[0]["text"] == "Which structure is FIFO?"
    assert questions[0]["options"] == ["Stack", "Queue", "Tree", "Graph"]
    assert questions[0]["page"] == 2
