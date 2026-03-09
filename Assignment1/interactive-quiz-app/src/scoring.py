# src/scoring.py
# ITM352 - Spring 2026 - Assignment 1
# Justin
#
# Functions for saving and loading scores.
# Scores are stored in data/scores.json so they persist between runs.

import json
import os

# Path to the scores file, sitting next to questions.json in data/.
SCORES_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "scores.json")


# Reads scores.json and returns all the data inside it.
# If the file doesn't exist yet or is broken, returns a clean
# empty structure so the rest of the code doesn't have to
# worry about getting None back.
def load_scores():
    # No file means nobody has played yet, so return a blank slate.
    if not os.path.exists(SCORES_FILE):
        return {"users": {}, "grand_champion": None}

    try:
        file = open(SCORES_FILE, "r")
        data = json.load(file)
        file.close()
        return data
    except:
        # Something went wrong reading the file, start fresh.
        return {"users": {}, "grand_champion": None}


# Saves a player's result after a game, updates their personal high
# score if they beat it, updates the grand champion if they beat
# that, then writes everything back to disk.
# Returns True if this score is a new personal high for that player.
def save_score(scores, username, category, score):
    # First time we've seen this name, create their entry.
    if username not in scores["users"]:
        scores["users"][username] = {
            "high_score": 0,
            "history": []
        }

    # Compare to their previous best to see if this is a new record.
    is_new_high = score > scores["users"][username]["high_score"]

    if is_new_high:
        scores["users"][username]["high_score"] = score

    # Append this game to the running history list for that player.
    game_record = {
        "score": score,
        "category": category
    }
    scores["users"][username]["history"].append(game_record)

    # Check if this score beats whoever is currently grand champion.
    current_champ = scores["grand_champion"]
    if current_champ is None or score > current_champ["score"]:
        scores["grand_champion"] = {"name": username, "score": score}

    # Make sure the data/ folder exists before writing.
    os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)
    file = open(SCORES_FILE, "w")
    json.dump(scores, file, indent=2)
    file.close()

    return is_new_high


# Returns the grand champion entry from the scores dict.
# That entry is a dict with a "name" key and a "score" key,
# or None if nobody has finished a game yet.
def get_grand_champion(scores):
    return scores["grand_champion"]
