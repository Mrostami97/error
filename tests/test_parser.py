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


def test_extracts_multiple_questions_on_one_page():
    text = """1. First question?
A. One
B. Two
C. Three
D. Four
2. Second question?
A. Alpha
B. Beta
C. Gamma
D. Delta
"""
    questions = extract_questions_from_text(text, page=7)
    assert [q["number"] for q in questions] == [1, 2]
    assert [q["page"] for q in questions] == [7, 7]


def test_supports_persian_question_and_option_digits():
    text = """۱۲. کدام گزینه درست است؟
۱) گزینه اول
۲) گزینه دوم
۳) گزینه سوم
۴) گزینه چهارم
"""
    questions = extract_questions_from_text(text, page=3)
    assert len(questions) == 1
    assert questions[0]["number"] == 12
    assert questions[0]["options"] == ["گزینه اول", "گزینه دوم", "گزینه سوم", "گزینه چهارم"]


def test_supports_arabic_indic_question_digits():
    text = """٣. Pick one.
A) First
B) Second
"""
    questions = extract_questions_from_text(text)
    assert questions[0]["number"] == 3
    assert questions[0]["options"] == ["First", "Second"]


def test_supports_numeric_option_labels():
    text = """5. Pick one.
1) First
2) Second
3) Third
4) Fourth
"""
    questions = extract_questions_from_text(text)
    assert len(questions) == 1
    assert questions[0]["options"] == ["First", "Second", "Third", "Fourth"]


def test_preserves_multiline_question_text_as_normalized_text():
    text = """8. This question starts here
and continues on the next line.
A. One
B. Two
"""
    questions = extract_questions_from_text(text)
    assert questions[0]["text"] == "This question starts here and continues on the next line."


def test_allows_questions_with_missing_options():
    text = """9. Short-answer-like block with no parsed options.
"""
    questions = extract_questions_from_text(text)
    assert len(questions) == 1
    assert questions[0]["options"] == []


def test_returns_empty_list_when_no_questions_are_detected():
    assert extract_questions_from_text("A title and some ordinary prose.") == []


def test_parenthesized_next_question_is_not_mistaken_for_numeric_option():
    text = """1) First question with no options.
2) Second question with no options.
"""
    questions = extract_questions_from_text(text)
    assert [q["number"] for q in questions] == [1, 2]
