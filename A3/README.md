# Quiz Arcade — A3

A single-page Flask quiz game with an arcade/neon theme.
Users pick a category, difficulty, and timed/untimed mode, answer a shuffled
batch of questions, and see their score against a persistent top-10
leaderboard and their own run history.

## Project layout

```
A3/
├── app.py              # Flask app + API routes
├── quiz_logic.py       # Pure functions: load, filter, shuffle, score
├── storage.py          # JSON read/write for leaderboard + history
├── data/
│   ├── questions.json  # Questions grouped by category
│   ├── leaderboard.json (created on first submit)
│   └── history.json    (created on first submit)
├── templates/
│   └── index.html      # Single-page app (all screens)
├── static/
│   ├── css/styles.css
│   └── js/quiz.js      # SPA state machine
├── tests/
│   ├── ExerciseAPI_test.py   # Route accessibility tests
│   └── test_quiz_logic.py    # Unit tests for quiz_logic
└── docs/
    └── REQUIREMENTS.md       # Maps each requirement to its code
```

## Setup

1. From the repo root, create and activate a virtual environment:
   ```
   python -m venv .venv
   .\.venv\Scripts\activate      # Windows
   source .venv/bin/activate     # macOS / Linux
   ```
2. Install dependencies:
   ```
   pip install flask pytest
   ```

## Running the app

From the `A3/` folder:
```
python app.py
```
Then open http://127.0.0.1:5000/ in a browser.

## Playing

1. Enter a name on the welcome screen (1–20 letters / numbers / spaces).
   On later visits the app remembers you via the session cookie.
2. Pick a category, difficulty (easy / medium / hard), and mode
   (timed 20s per question, or untimed).
3. Answer the shuffled questions. Points: easy = 1, medium = 2, hard = 3.
4. The results screen shows your score, percentage, rank on the leaderboard,
   and whether it's a new personal best.
5. Use the results screen buttons to view the high-score leaderboard or your
   own run history.

## API routes

| Method | Path                 | What it does                                     |
|------- |----------------------|--------------------------------------------------|
| GET    | `/`                  | Serve the single-page app                         |
| POST   | `/api/set-name`      | Save `{username}` to session; validates the name |
| GET    | `/api/categories`    | List of category names                            |
| GET    | `/api/questions`     | Shuffled questions (`?category=&difficulty=`)     |
| POST   | `/api/submit-score`  | Save a finished run; returns entry + rank         |
| GET    | `/api/leaderboard`   | Top 10 entries across all users                   |
| GET    | `/api/history`       | Run history for the current session user          |

## Tests

From the `A3/` folder:
```
python -m pytest tests/ -v
```
- `tests/ExerciseAPI_test.py` — hits each route through the Flask test client
  and checks status codes and response shapes.
- `tests/test_quiz_logic.py` — unit tests for `calculate_points`,
  `filter_by_difficulty`, `shuffle_questions`, `get_categories`, and
  `get_quiz_questions`.

## Adding questions

Edit [data/questions.json](data/questions.json). Each question needs:
```json
{
  "question": "...",
  "options": ["a) ...", "b) ...", "c) ...", "d) ..."],
  "correct": ["c"],
  "hint": "...",
  "explanation": "...",
  "difficulty": "easy"
}
```
`correct` is a list so multi-answer questions work the same way.
