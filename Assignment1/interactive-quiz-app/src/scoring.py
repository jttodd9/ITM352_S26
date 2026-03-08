# src/scoring.py
# ITM352 - Spring 2026 - Assignment 1
# Justin
#
# Handles reading and writing the scores file. I broke this out into its
# own module so quiz.py doesn't have to deal with file I/O at all.
#
# The scores are saved as JSON in data/scores.json. I chose JSON over a
# plain text file because it made it easy to store structured data like
# the history list and grand champion without having to write a custom parser.

import json
import os
from datetime import datetime

# Keep scores next to questions.json in the data folder
SCORES_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "scores.json")


def load_scores():
    """
    Reads scores.json and returns the data as a dict. If the file doesn't
    exist yet (first run) or is somehow broken, we just return an empty
    structure so the rest of the program doesn't have to handle None checks.
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
    Records a completed game for a player. Updates their history list,
    their personal high score if they beat it, and the grand champion
    record if they beat that too. Then writes everything back to disk.

    Returns True if this was a new personal high score, so quiz.py
    knows whether to show the congratulations message.
    """
    # First time we've seen this username -- set them up
    if username not in scores["users"]:
        scores["users"][username] = {
            "high_score": 0,
            "history": []
        }

    user_data = scores["users"][username]
    is_new_high = score > user_data["high_score"]

    if is_new_high:
        user_data["high_score"] = score

    # Add this game to their history with a timestamp
    user_data["history"].append({
        "score": score,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    # See if they beat the all-time record
    _update_grand_champion(scores, username, score)

    # Write to disk -- makedirs handles the case where data/ doesn't exist yet
    os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)

    return is_new_high


def get_high_score(scores, username):
    """Returns a player's personal best, or 0 if they haven't played before."""
    if username in scores["users"]:
        return scores["users"][username]["high_score"]
    return 0


def get_grand_champion(scores):
    """
    Returns the grand champion entry (a dict with 'name' and 'score'),
    or None if nobody has played yet.
    """
    return scores.get("grand_champion")


def _update_grand_champion(scores, username, score):
    """
    Checks if this score beats the current grand champion and updates
    the record if so. Called internally by save_score every time a game ends.
    """
    current_champ = scores.get("grand_champion")
    if current_champ is None or score > current_champ["score"]:
        scores["grand_champion"] = {"name": username, "score": score}
