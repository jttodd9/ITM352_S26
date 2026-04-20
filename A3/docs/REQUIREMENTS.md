# Requirements Map

This document maps each requirement from the assignment to the file(s) and
function(s) that satisfy it.

## Functional Requirements

### 1. Welcome and user identification
- A welcome screen greets the user and asks for a name.
  - [templates/index.html](../templates/index.html) — `#screen-welcome`
- Returning users (session cookie) see a "Welcome back" message.
  - [static/js/quiz.js](../static/js/quiz.js) — `showWelcomeScreen()` checks `window.INITIAL_USERNAME`.
- Name is validated (1–20 letters, numbers, or spaces).
  - [app.py](../app.py) — `NAME_PATTERN` in `set_name()`.

### 2. Category + difficulty + mode selection
- User chooses category (from `questions.json`), difficulty (easy/medium/hard),
  and mode (timed/untimed).
  - [templates/index.html](../templates/index.html) — `#screen-setup`.
  - [static/js/quiz.js](../static/js/quiz.js) — setup chip handlers + `BEGIN QUIZ` button.

### 3. Question delivery
- Questions served from a JSON file grouped by category.
  - [data/questions.json](../data/questions.json)
  - [quiz_logic.py](../quiz_logic.py) — `load_questions()`, `get_quiz_questions()`.
- Questions are filtered by difficulty and shuffled.
  - [quiz_logic.py](../quiz_logic.py) — `filter_by_difficulty()`, `shuffle_questions()`.
- Each question includes a hint and explanation.
  - See fields `hint` and `explanation` in [data/questions.json](../data/questions.json).

### 4. Multiple-choice + multi-answer handling
- Each question supplies a list of options; `correct` is a list so multi-answer
  is supported.
  - [data/questions.json](../data/questions.json) — each question has `correct: []`.
  - [static/js/quiz.js](../static/js/quiz.js) — option handler compares the user's
    selection(s) against `q.correct`.

### 5. Scoring
- Points by difficulty: easy = 1, medium = 2, hard = 3.
  - [quiz_logic.py](../quiz_logic.py) — `calculate_points()`, `POINTS` dict.
- Running score is shown in the quiz HUD.
  - [templates/index.html](../templates/index.html) — `#hud-score`.
  - [static/js/quiz.js](../static/js/quiz.js) — score update in answer handler.

### 6. Timed mode
- Timed mode enforces a 20-second limit per question with a visible ring timer.
  - [templates/index.html](../templates/index.html) — `#hud-timer` SVG ring.
  - [static/js/quiz.js](../static/js/quiz.js) — `startTimer()` / `stopTimer()`.

### 7. Results and feedback
- After the last question a results screen shows score, total possible,
  percent, rank, and a "personal best" flag when applicable.
  - [templates/index.html](../templates/index.html) — `#screen-results`.
  - [static/js/quiz.js](../static/js/quiz.js) — `showResults()` + history check.
- The server computes percentage and timestamp at submit time.
  - [app.py](../app.py) — `submit_score()`.

### 8. Leaderboard (persistent, top 10)
- Top 10 saved across sessions in JSON, sorted by percentage then raw score.
  - [storage.py](../storage.py) — `save_score()`, `get_leaderboard()`, `LEADERBOARD_LIMIT`.
  - `data/leaderboard.json` (created on first submit).

### 9. Per-user history
- Each user's full run history is kept in a separate JSON file, newest first.
  - [storage.py](../storage.py) — `get_history()`, `save_score()`.
  - `data/history.json` (created on first submit).

### 10. Single-page navigation
- All screens (welcome / setup / quiz / results / leaderboard / history) live in
  one `index.html`; the JS state machine shows one at a time.
  - [templates/index.html](../templates/index.html)
  - [static/js/quiz.js](../static/js/quiz.js) — `showScreen()`.

## Non-Functional Requirements

### API is RESTful and JSON
- All data routes accept/return JSON.
  - [app.py](../app.py) — `/api/set-name`, `/api/categories`, `/api/questions`,
    `/api/submit-score`, `/api/leaderboard`, `/api/history`.

### Session handling
- Flask session cookie holds the current username between screens and visits.
  - [app.py](../app.py) — `session["username"]` in `set_name()`, `index()`,
    `submit_score()`, `history()`.

### Separation of concerns
- Routing / HTTP → `app.py`.
- Quiz rules (points, filtering, shuffling) → `quiz_logic.py`.
- Persistence (leaderboard, history files) → `storage.py`.
- Presentation → `templates/` + `static/`.

### Accessibility / usability
- Keyboard-reachable buttons, high-contrast arcade theme, clear error messages
  for name + setup validation.
  - [static/css/styles.css](../static/css/styles.css).
  - [static/js/quiz.js](../static/js/quiz.js) — error banners, `#name-error`,
    `#setup-error`.

### Testing
- Route tests verify every API endpoint is reachable and returns the expected
  shape/status.
  - [tests/ExerciseAPI_test.py](../tests/ExerciseAPI_test.py)
- Unit tests cover the pure quiz-logic functions.
  - [tests/test_quiz_logic.py](../tests/test_quiz_logic.py)
- Run: `python -m pytest tests/ -v` from inside `A3/`.
