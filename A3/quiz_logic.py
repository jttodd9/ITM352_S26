# quiz_logic.py - Pure functions for loading and working with questions.

import json
import os
import random

# Path to the questions file (lives in A3/data/questions.json).
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "data", "questions.json")

# Points awarded per correct answer by difficulty.
POINTS = {"easy": 1, "medium": 2, "hard": 3}


def load_questions():
    """Load all questions grouped by category from the JSON file."""
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["categories"]


def get_categories():
    """Return a list of category names."""
    categories = load_questions()
    return list(categories.keys())


def filter_by_difficulty(questions, difficulty):
    """Return only the questions that match the given difficulty."""
    return [q for q in questions if q.get("difficulty") == difficulty]


def shuffle_questions(questions):
    """Return a new list of the questions in random order."""
    shuffled = list(questions)
    random.shuffle(shuffled)
    return shuffled


def calculate_points(difficulty):
    """Return the point value for a question of the given difficulty."""
    return POINTS.get(difficulty, 1)


def get_quiz_questions(category, difficulty):
    """Get shuffled questions for a category and difficulty."""
    all_questions = load_questions()
    if category not in all_questions:
        return []
    filtered = filter_by_difficulty(all_questions[category], difficulty)
    return shuffle_questions(filtered)
