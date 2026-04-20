# test_quiz_logic.py - Unit tests for the quiz_logic pure functions.
# Run with:  python -m pytest A3/tests/test_quiz_logic.py -v

import os
import sys

# Make the A3 package importable when running from the repo root or from A3/.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import quiz_logic  # noqa: E402


def test_calculate_points_easy():
    assert quiz_logic.calculate_points("easy") == 1


def test_calculate_points_medium():
    assert quiz_logic.calculate_points("medium") == 2


def test_calculate_points_hard():
    assert quiz_logic.calculate_points("hard") == 3


def test_calculate_points_unknown_defaults_to_one():
    assert quiz_logic.calculate_points("impossible") == 1


def test_load_questions_returns_dict():
    data = quiz_logic.load_questions()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_get_categories_is_nonempty_list():
    categories = quiz_logic.get_categories()
    assert isinstance(categories, list)
    assert len(categories) > 0
    for name in categories:
        assert isinstance(name, str)


def test_filter_by_difficulty_only_returns_matching():
    sample = [
        {"question": "q1", "difficulty": "easy"},
        {"question": "q2", "difficulty": "medium"},
        {"question": "q3", "difficulty": "easy"},
        {"question": "q4", "difficulty": "hard"},
    ]
    easy = quiz_logic.filter_by_difficulty(sample, "easy")
    assert len(easy) == 2
    assert all(q["difficulty"] == "easy" for q in easy)


def test_filter_by_difficulty_empty_when_no_match():
    sample = [{"question": "q1", "difficulty": "easy"}]
    assert quiz_logic.filter_by_difficulty(sample, "hard") == []


def test_shuffle_questions_preserves_items():
    sample = [{"id": i} for i in range(20)]
    shuffled = quiz_logic.shuffle_questions(sample)
    assert len(shuffled) == len(sample)
    assert sorted(q["id"] for q in shuffled) == list(range(20))


def test_shuffle_questions_does_not_mutate_input():
    sample = [{"id": i} for i in range(10)]
    original_order = [q["id"] for q in sample]
    quiz_logic.shuffle_questions(sample)
    assert [q["id"] for q in sample] == original_order


def test_get_quiz_questions_unknown_category():
    assert quiz_logic.get_quiz_questions("not_a_real_category", "easy") == []


def test_get_quiz_questions_returns_matching_difficulty():
    categories = quiz_logic.get_categories()
    assert categories, "Need at least one category for this test"
    cat = categories[0]
    qs = quiz_logic.get_quiz_questions(cat, "easy")
    assert isinstance(qs, list)
    for q in qs:
        assert q["difficulty"] == "easy"
