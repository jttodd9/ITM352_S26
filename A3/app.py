# app.py - Flask web app for the quiz game.

import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session

import quiz_logic
import storage

app = Flask(__name__)
app.secret_key = "itm352-quiz-arcade-secret"

NAME_PATTERN = re.compile(r"^[A-Za-z0-9 ]{1,20}$")


@app.route("/")
def index():
    """Serve the single page app."""
    username = session.get("username", "")
    return render_template("index.html", username=username)


@app.route("/api/set-name", methods=["POST"])
def set_name():
    """Save a username to the session."""
    data = request.get_json() or {}
    name = (data.get("username") or "").strip()
    if not NAME_PATTERN.match(name):
        return jsonify({"error": "Name must be 1-20 letters, numbers, or spaces."}), 400
    session["username"] = name
    return jsonify({"username": name})


@app.route("/api/categories")
def categories():
    """Return list of category names."""
    return jsonify({"categories": quiz_logic.get_categories()})


@app.route("/api/questions")
def questions():
    """Return shuffled questions for a category + difficulty."""
    category = request.args.get("category")
    difficulty = request.args.get("difficulty")
    if not category or not difficulty:
        return jsonify({"error": "Please pick a category and difficulty."}), 400

    qs = quiz_logic.get_quiz_questions(category, difficulty)
    if not qs:
        return jsonify({"error": "No questions found for that choice."}), 404

    # Attach points for each question so the client can total it
    for q in qs:
        q["points"] = quiz_logic.calculate_points(q["difficulty"])

    return jsonify({"questions": qs})


@app.route("/api/submit-score", methods=["POST"])
def submit_score():
    """Save a completed quiz score."""
    username = session.get("username")
    if not username:
        return jsonify({"error": "No user set. Please enter a name first."}), 400

    data = request.get_json() or {}
    required = ["score", "total_possible", "category", "difficulty", "timed"]
    for key in required:
        if key not in data:
            return jsonify({"error": f"Missing field: {key}"}), 400

    total = data["total_possible"] or 1
    percentage = round(data["score"] / total * 100)

    entry = {
        "username": username,
        "score": data["score"],
        "total_possible": data["total_possible"],
        "percentage": percentage,
        "category": data["category"],
        "difficulty": data["difficulty"],
        "timed": bool(data["timed"]),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    leaderboard = storage.save_score(entry)

    # Find rank, if on the board
    rank = None
    for i, e in enumerate(leaderboard, start=1):
        if e["timestamp"] == entry["timestamp"] and e["username"] == entry["username"]:
            rank = i
            break

    return jsonify({"entry": entry, "rank": rank})


@app.route("/api/leaderboard")
def leaderboard():
    """Return the top 10 leaderboard entries."""
    return jsonify({"entries": storage.get_leaderboard()})


@app.route("/api/history")
def history():
    """Return the current user's score history."""
    username = session.get("username")
    if not username:
        return jsonify({"history": []})
    return jsonify({"history": storage.get_history(username)})


if __name__ == "__main__":
    app.run(debug=True)
