# src/scoring.py
# ============================================================
# Scoring Module - ITM352 Spring 2026 - Assignment 1
#
# Handles all score persistence:
#   - Load / save scores from a JSON file (requirement 1)
#   - Track personal high scores per user (extra credit)
#   - Determine and store the grand champion (extra credit)
# ============================================================

import json
import os
from datetime import datetime

# Score file lives in the data/ directory next to questions.json
SCORES_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "scores.json")


def load_scores():
    """
    Load the scores database from the JSON file.

    If the file does not exist or cannot be parsed, returns a blank structure.

    Returns:
        dict: {
            "users": {
                "<username>": {
                    "high_score": int,
                    "history": [{"score": int, "category": str, "date": str}, ...]
                }
            },
            "grand_champion": {"name": str, "score": int} | None
        }
    """
    if not os.path.exists(SCORES_FILE):
        return {"users": {}, "grand_champion": None}

    try:
        with open(SCORES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"users": {}, "grand_champion": None}


def save_score(scores, username, category, score):
    """
    Record a completed game, updating the user's history, personal high score,
    and the overall grand champion. Writes the updated data back to disk.

    Args:
        scores (dict):   The current scores dict (from load_scores).
        username (str):  The player's name.
        category (str):  The quiz category that was played.
        score (int):     The total score (base + bonus) achieved.

    Returns:
        bool: True if this score is a new personal high score for the user.
    """
    # Create a fresh entry for first-time users
    if username not in scores["users"]:
        scores["users"][username] = {
            "high_score": 0,
            "history": []
        }

    user_data = scores["users"][username]
    is_new_high = score > user_data["high_score"]

    if is_new_high:
        user_data["high_score"] = score

    # Append this game to the user's history log
    user_data["history"].append({
        "score": score,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    # Check whether this score beats the grand champion record
    _update_grand_champion(scores, username, score)

    # Write everything to disk
    os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)

    return is_new_high


def get_high_score(scores, username):
    """
    Return the personal high score for a given username.

    Args:
        scores (dict): The loaded scores dictionary.
        username (str): The player's name.

    Returns:
        int: The player's highest score, or 0 if they have no record.
    """
    if username in scores["users"]:
        return scores["users"][username]["high_score"]
    return 0


def get_grand_champion(scores):
    """
    Return the current grand champion entry.

    Returns:
        dict | None: {"name": str, "score": int}, or None if no games played yet.
    """
    return scores.get("grand_champion")


def _update_grand_champion(scores, username, score):
    """
    Update the grand champion record if the given score beats it.

    Args:
        scores (dict):   The full scores dictionary (modified in place).
        username (str):  The player's name.
        score (int):     The score to compare.
    """
    current_champ = scores.get("grand_champion")
    if current_champ is None or score > current_champ["score"]:
        scores["grand_champion"] = {"name": username, "score": score}
