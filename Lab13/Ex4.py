import json
import os

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "dev-skeleton-key-change-me"

QUESTIONS_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "Assignment1",
    "interactive-quiz-app",
    "data",
    "questions.json",
)


def load_questions():
    try:
        with open(QUESTIONS_FILE, "r") as f:
            return json.load(f)["categories"]
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


@app.route("/")
def index():
    return render_template("quiz_index.html")


@app.route("/start", methods=["POST"])
def start():
    username = request.form.get("username", "").strip() or "guest"
    session["username"] = username
    session["score"] = 0
    session["q_index"] = 0
    session["category"] = None
    return redirect(url_for("choose_category"))


@app.route("/categories")
def choose_category():
    categories = load_questions()
    return render_template("quiz_categories.html", categories=list(categories.keys()))


@app.route("/category/<name>")
def pick_category(name):
    session["category"] = name
    session["score"] = 0
    session["q_index"] = 0
    return redirect(url_for("question"))


@app.route("/question", methods=["GET", "POST"])
def question():
    categories = load_questions()
    cat = session.get("category")
    if not cat or cat not in categories:
        return redirect(url_for("index"))

    questions = categories[cat]
    idx = session.get("q_index", 0)

    if request.method == "POST":
        answer = request.form.get("answer", "").strip().lower()
        correct = questions[idx]["correct"]
        if sorted([answer]) == sorted(correct):
            session["score"] = session.get("score", 0) + 1
        session["q_index"] = idx + 1
        if session["q_index"] >= len(questions):
            return redirect(url_for("results"))
        return redirect(url_for("question"))

    current = questions[idx]
    return render_template(
        "quiz_question.html",
        question=current,
        number=idx + 1,
        total=len(questions),
        score=session.get("score", 0),
    )


@app.route("/results")
def results():
    return render_template(
        "quiz_results.html",
        username=session.get("username", "guest"),
        score=session.get("score", 0),
        category=session.get("category", ""),
    )


if __name__ == "__main__":
    app.run(debug=True)
