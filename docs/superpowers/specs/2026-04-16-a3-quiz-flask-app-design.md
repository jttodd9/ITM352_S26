# A3 — Quiz Game Flask Web App — Design Spec

**Date:** 2026-04-16
**Author:** Justin Todd (ITM 352, Spring 2026)
**Source material:** `Assignment1/interactive_quiz.py` and `Assignment1/data/questions.json`
**Location of new work:** `A3/`

---

## 1. Goal

Convert the terminal-based interactive quiz game from Assignment 1 into a Flask web application with a single-page (SPA-lite) user experience. Meet all core functional and non-functional requirements from the A3 assignment, plus these four individual requirements:

1. **Persistent User Identification and History** — session cookie remembers the user; their past scores are shown on return.
2. **Leaderboard System** — global top 10, persisted to disk.
3. **Timer-Based Challenge Mode** — per-question 20-second countdown with auto-advance on timeout; users can also choose an untimed mode.
4. **Difficulty Levels** — Easy / Medium / Hard, with scoring scaled per question (1 / 2 / 3 points).

## 2. Stack & Constraints

- **Backend:** Flask 3.x, Python 3.11+.
- **Frontend:** Plain HTML + CSS + vanilla JavaScript (no framework, no build step).
- **Persistence:** JSON files on disk (no database).
- **Style:** Beginner-level code. Straightforward control flow, minimal abstraction, function-level docstrings, no cleverness for its own sake.

## 3. Project Structure

```
A3/
├── app.py                     # Flask app: routes + API endpoints
├── quiz_logic.py              # Pure functions: load questions, shuffle, score
├── storage.py                 # Read/write leaderboard.json + history.json
├── data/
│   ├── questions.json         # From Assignment1; each question tagged with difficulty
│   ├── leaderboard.json       # Global top-10 list
│   └── history.json           # Score history keyed by username
├── static/
│   ├── css/styles.css         # Arcade aesthetic
│   ├── js/quiz.js             # SPA state machine, timer, API calls
│   └── fonts/                 # Self-hosted pixel + mono fonts
├── templates/
│   └── index.html             # Single Jinja template; JS swaps screens
├── tests/
│   ├── test_api.py            # Flask route integration tests
│   ├── test_quiz_logic.py     # Pure-logic unit tests
│   └── test_storage.py        # JSON read/write tests
├── docs/
│   ├── requirements_satisfied.md
│   └── use_of_ai.md
├── requirements.txt
└── README.md
```

The existing empty `A3/R1.py` will be deleted.

## 4. Data Model

### `data/questions.json`

Existing Assignment 1 shape, with one added field per question: `"difficulty": "easy" | "medium" | "hard"`.

```json
{
  "categories": {
    "history": [
      {
        "question": "In what year did World War II end?",
        "options": ["a) 1943", "b) 1944", "c) 1945", "d) 1946"],
        "correct": ["c"],
        "hint": "It was in the mid-1940s.",
        "explanation": "WWII ended in 1945...",
        "difficulty": "medium"
      }
    ]
  }
}
```

All existing questions become `"medium"`. 2-3 easy and 2-3 hard questions will be added per category so every difficulty has real content.

### `data/leaderboard.json`

Flat list of top entries, sorted by score (with percentage as tiebreaker). Capped at 10 entries.

```json
{
  "entries": [
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
  ]
}
```

### `data/history.json`

Keyed by username, list of past attempts newest-first.

```json
{
  "Justin": [
    {
      "score": 14,
      "total_possible": 18,
      "percentage": 77,
      "category": "science",
      "difficulty": "hard",
      "timed": true,
      "timestamp": "2026-04-16T14:32:01"
    }
  ]
}
```

### Session cookie

`session["username"]` — nothing else. History is looked up server-side by username.

### Scoring

- Easy question correct: 1 point
- Medium question correct: 2 points
- Hard question correct: 3 points
- `total_possible` = sum of point values for all presented questions.
- `percentage` = round(`score` / `total_possible` * 100).

## 5. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Serve `index.html` |
| POST | `/api/set-name` | Save `{"username": "..."}` to session |
| GET | `/api/categories` | List category names |
| GET | `/api/questions?category=X&difficulty=Y` | Randomized questions incl. correct answers |
| POST | `/api/submit-score` | Save final score to history + leaderboard |
| GET | `/api/leaderboard` | Return top 10 |
| GET | `/api/history` | Return current user's history |

### Design choice: correct answers sent with questions

The client receives correct answers inside the `/api/questions` payload and validates each choice in JavaScript. This is the beginner-standard approach (matches most Flask quiz tutorials). Trade-off: a determined user could inspect the network tab and cheat; acceptable here since this is a learning exercise, not a graded assessment system.

## 6. Client-Side Flow (SPA State Machine)

One `index.html`, six `<section>` screens, one visible at a time. JavaScript `showScreen(name)` toggles visibility.

```
  Welcome
     │  POST /api/set-name  (new user)
     │  or session already has name (returning user → show history preview)
     ▼
  Setup (pick category, difficulty, timed/untimed)
     │  GET /api/questions?category=X&difficulty=Y
     ▼
  Quiz  (per question):
     │    show question + options
     │    if timed: 20s countdown; auto-submit blank on timeout
     │    user clicks an option
     │    client checks against correct answers
     │    green flash + ✓ or red flash + ✗ with explanation (~2s)
     │    advance to next question
     │  after last question: POST /api/submit-score
     ▼
  Results (score, %, rank, new PB?)
     │  buttons: Play Again | Leaderboard | History
     ▼
  Leaderboard  (GET /api/leaderboard)
  History      (GET /api/history)
```

## 7. UI / Visual Design — Arcade Aesthetic

### Typography

- **Display font:** "Press Start 2P" (pixel, self-hosted).
- **Body/mono font:** "VT323" or "Share Tech Mono" (self-hosted).

### Colors (CSS custom properties)

```css
--bg-black:     #0a0a0f;
--neon-green:   #39ff14;   /* primary accent */
--neon-magenta: #ff2bd6;   /* secondary accent, timer urgency */
--neon-cyan:    #00e5ff;   /* info, hover */
--warn-red:     #ff3355;   /* incorrect, timer < 5s */
--dim-green:    #1a4d2e;   /* muted borders */
--text-main:    #e8f5e8;
```

### Atmosphere

- CRT scanline overlay (repeating linear-gradient, `pointer-events: none`).
- Neon glow via `text-shadow` and `box-shadow`.
- Optional noise background (tiny tiled SVG or PNG).
- Sharp 1-2px neon borders; no rounded corners; no gradients-on-white; no purple.

### Screens

1. **Welcome** — flickering "QUIZ ARCADE" title. Returning users see "WELCOME BACK, NAME". New users enter a name.
2. **Setup** — arcade-menu selectors for CATEGORY / DIFFICULTY / MODE, plus a START button.
3. **Quiz** — top bar: `SCORE: 008`, `Q 3/6`. Circular SVG timer ring (magenta; turns red under 5s). Four option buttons with A/B/C/D prefixes. Correct → green flash + ✓; incorrect → red flash + ✗ + shake; explanation in cyan; auto-advance ~2s.
4. **Results** — odometer count-up on score. Lines: `ACCURACY: 83%`, `RANK: #3`, `NEW PERSONAL BEST!` if applicable. Buttons: Play Again / Leaderboard / History.
5. **Leaderboard** — arcade high-score-table styling. Gold/silver/bronze text-shadow on top 3.
6. **History** — newest-first log: `2026-04-16 • SCIENCE / HARD / TIMED • 14/18 (77%)`.

### Motion

- Screen transition: ~250ms horizontal scanline sweep.
- Timer ring: SVG stroke-dashoffset animation; pulsing glow under 5s.
- Correct: neon-green flash + slight scale bump.
- Incorrect: red flash + 3-frame shake.
- Button hover: glow intensifies.
- Page load: staggered fade-in (50ms between elements).

### Accessibility basics

- Real `<button>` elements; keyboard navigable.
- Color never the only signal — ✓/✗ icons accompany correct/incorrect.
- Timer ring shows a text number alongside the graphic.
- Minimum body font size 16px.

## 8. Error Handling

Beginner-simple — no elaborate error taxonomy.

- Wrap all file reads in `try/except FileNotFoundError` and `except json.JSONDecodeError`.
- Missing `leaderboard.json` or `history.json` → create empty file on first write.
- Missing `questions.json` → return 500 with `{"error": "Questions could not be loaded."}`; client shows a generic "Something went wrong" screen.
- Missing query params on `/api/questions` → 400 with `{"error": "Please pick a category."}`.
- Name validation: trim whitespace, require 1-20 chars, `[A-Za-z0-9 ]` only. Invalid name → inline error on the welcome screen.
- Every `fetch()` on the client has a `.catch()` that shows a single "Connection error — try again" banner.

## 9. Testing Strategy

All tests use `pytest`. No mocks for the filesystem — tests use `tmp_path` and point `storage.py` at temp JSON files via a module-level path constant or a fixture that monkeypatches it.

### `tests/test_quiz_logic.py`

- `load_questions()` returns expected structure.
- `filter_by_difficulty()` returns only questions matching difficulty.
- `shuffle_questions()` preserves length and content.
- `calculate_points(difficulty)` returns 1 / 2 / 3.

### `tests/test_storage.py`

- `save_score()` appends to history for the correct user.
- `save_score()` updates leaderboard and caps it at 10.
- `get_leaderboard()` returns a properly sorted list.
- `get_history(username)` returns only that user's entries.

### `tests/test_api.py` (satisfies the "ExerciseAPI_test.py" requirement)

- `GET /` returns 200 and the HTML page.
- `POST /api/set-name` stores the username in session.
- `GET /api/questions?category=science&difficulty=easy` returns questions.
- `GET /api/questions` with missing params returns 400.
- `POST /api/submit-score` saves successfully.
- `GET /api/leaderboard` returns the list.
- `GET /api/history` returns current user's entries.

## 10. Documentation Deliverables

- **`A3/README.md`** — setup, run, and play instructions.
- **`A3/docs/requirements_satisfied.md`** — every functional/non-functional requirement and every individual requirement, with a 1-2 sentence note on how it's satisfied and where in the code it lives.
- **`A3/docs/use_of_ai.md`** — honest writeup of AI usage: which functions were AI-drafted, the prompts used, what was adjusted, what was verified.

Code comments: function-level docstrings only. No line-by-line over-commenting. AI-drafted functions get one top-of-function note like `# Drafted with Claude; adapted to match our JSON shape.`

## 11. Requirement Mapping Preview

| Assignment requirement | Where it's satisfied |
|---|---|
| UI with HTML/CSS/JS | `templates/index.html`, `static/css/styles.css`, `static/js/quiz.js` |
| Dynamic elements respond to user | `quiz.js` (click handlers, timer, screen transitions) |
| Load questions from JSON (not hard-coded) | `quiz_logic.load_questions()` reads `data/questions.json` |
| Randomize question + answer order | `quiz_logic.shuffle_questions()` on each session |
| Real-time answer feedback | Client-side check in `quiz.js`; green/red flash + explanation |
| Score tracking | Client-side accumulator; final `POST /api/submit-score` |
| Server-side data storage | `storage.py` reads/writes JSON files |
| Flask framework | `app.py` |
| RESTful APIs | `/api/questions`, `/api/submit-score`, `/api/leaderboard`, `/api/history` |
| Final score + feedback | Results screen shows score, %, rank, PB |
| Input validation | Name validation; query-param checks |
| User-friendly error messages | Inline errors on welcome; generic connection banner |
| **R1 Persistent user + history** | `session["username"]` + `history.json`; Welcome screen recognizes returning users |
| **R2 Leaderboard** | `leaderboard.json`, top 10 screen |
| **R3 Timer mode** | 20s per-question countdown in `quiz.js`; user toggles at setup |
| **R4 Difficulty levels** | `difficulty` field on each question; setup selector; scaled scoring |
| Documentation | README + `requirements_satisfied.md` + `use_of_ai.md` |
| Testing | `pytest` suite in `tests/` |
| Maintainability | Three small modules (`app.py`, `quiz_logic.py`, `storage.py`), each focused |
