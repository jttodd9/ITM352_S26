# storage.py - Reads and writes the leaderboard and history JSON files.

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
LEADERBOARD_FILE = os.path.join(DATA_DIR, "leaderboard.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

LEADERBOARD_LIMIT = 10


def _read_json(path, default):
    """Read a JSON file, return default if missing or empty."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _write_json(path, data):
    """Write a dict/list to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_leaderboard():
    """Return the list of leaderboard entries (top first)."""
    data = _read_json(LEADERBOARD_FILE, {"entries": []})
    return data.get("entries", [])


def get_history(username):
    """Return score history for a given user, newest first."""
    data = _read_json(HISTORY_FILE, {})
    return data.get(username, [])


def save_score(entry):
    """Save a score to both history and the leaderboard.

    entry should be a dict like:
    {
        "username": "Justin",
        "score": 14,
        "total_possible": 18,
        "percentage": 77,
        "category": "science",
        "difficulty": "hard",
        "timed": true,
        "timestamp": "2026-04-16T14:32:01"
    }
    """
    # Update history
    history = _read_json(HISTORY_FILE, {})
    username = entry["username"]
    if username not in history:
        history[username] = []
    # Newest first
    history[username].insert(0, entry)
    _write_json(HISTORY_FILE, history)

    # Update leaderboard
    leaderboard = _read_json(LEADERBOARD_FILE, {"entries": []})
    entries = leaderboard.get("entries", [])
    entries.append(entry)
    # Sort by percentage first, then score, both descending
    entries.sort(key=lambda e: (e["percentage"], e["score"]), reverse=True)
    # Keep only top 10
    entries = entries[:LEADERBOARD_LIMIT]
    _write_json(LEADERBOARD_FILE, {"entries": entries})

    return entries
