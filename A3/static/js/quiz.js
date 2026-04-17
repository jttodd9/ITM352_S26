// quiz.js - SPA state machine, timer, and API calls for the quiz game.

// App state
const state = {
    username: window.INITIAL_USERNAME || "",
    category: null,
    difficulty: null,
    timed: null,
    questions: [],
    currentIndex: 0,
    score: 0,
    totalPossible: 0,
    timer: null,
    timeLeft: 20,
};

// ------------- Screen switching -------------

function showScreen(name) {
    document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
    document.getElementById("screen-" + name).classList.add("active");
}

// ------------- Helpers -------------

function showError(msg) {
    const banner = document.getElementById("error-banner");
    banner.textContent = msg;
    banner.classList.remove("hidden");
    setTimeout(() => banner.classList.add("hidden"), 3000);
}

function padScore(n) {
    return String(n).padStart(3, "0");
}

// ------------- Welcome screen -------------

function setupWelcome() {
    const returningUser = document.getElementById("returning-user");
    const newUser = document.getElementById("new-user");

    if (state.username) {
        returningUser.classList.remove("hidden");
        newUser.classList.add("hidden");
        document.getElementById("returning-name").textContent = state.username.toUpperCase();
    } else {
        returningUser.classList.add("hidden");
        newUser.classList.remove("hidden");
    }

    document.getElementById("btn-start").onclick = submitName;
    document.getElementById("input-name").onkeydown = (e) => {
        if (e.key === "Enter") submitName();
    };
    document.getElementById("btn-continue").onclick = () => {
        loadCategories();
        showScreen("setup");
    };
    document.getElementById("btn-change-name").onclick = () => {
        state.username = "";
        setupWelcome();
    };
}

function submitName() {
    const name = document.getElementById("input-name").value.trim();
    const errorEl = document.getElementById("name-error");
    if (!/^[A-Za-z0-9 ]{1,20}$/.test(name)) {
        errorEl.textContent = "Name must be 1-20 letters, numbers, or spaces.";
        errorEl.classList.remove("hidden");
        return;
    }
    errorEl.classList.add("hidden");

    fetch("/api/set-name", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: name}),
    })
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                errorEl.textContent = data.error;
                errorEl.classList.remove("hidden");
                return;
            }
            state.username = data.username;
            loadCategories();
            showScreen("setup");
        })
        .catch(() => showError("Connection error - try again"));
}

// ------------- Setup screen -------------

function loadCategories() {
    fetch("/api/categories")
        .then(r => r.json())
        .then(data => {
            const row = document.getElementById("category-options");
            row.innerHTML = "";
            data.categories.forEach(cat => {
                const btn = document.createElement("button");
                btn.className = "chip";
                btn.dataset.category = cat;
                btn.textContent = cat.toUpperCase();
                btn.onclick = () => selectCategory(cat, btn);
                row.appendChild(btn);
            });
        })
        .catch(() => showError("Connection error - try again"));
}

function selectCategory(cat, btn) {
    state.category = cat;
    document.querySelectorAll("#category-options .chip").forEach(c => c.classList.remove("selected"));
    btn.classList.add("selected");
    updateBeginButton();
}

function setupSetup() {
    document.querySelectorAll(".chip[data-difficulty]").forEach(btn => {
        btn.onclick = () => {
            state.difficulty = btn.dataset.difficulty;
            document.querySelectorAll(".chip[data-difficulty]").forEach(c => c.classList.remove("selected"));
            btn.classList.add("selected");
            updateBeginButton();
        };
    });
    document.querySelectorAll(".chip[data-timed]").forEach(btn => {
        btn.onclick = () => {
            state.timed = btn.dataset.timed === "true";
            document.querySelectorAll(".chip[data-timed]").forEach(c => c.classList.remove("selected"));
            btn.classList.add("selected");
            updateBeginButton();
        };
    });
    document.getElementById("btn-begin").onclick = beginQuiz;
}

function updateBeginButton() {
    const ready = state.category && state.difficulty && state.timed !== null;
    document.getElementById("btn-begin").disabled = !ready;
}

// ------------- Quiz screen -------------

function beginQuiz() {
    const url = `/api/questions?category=${encodeURIComponent(state.category)}&difficulty=${encodeURIComponent(state.difficulty)}`;
    fetch(url)
        .then(r => r.json().then(data => ({ok: r.ok, data})))
        .then(({ok, data}) => {
            if (!ok || data.error) {
                document.getElementById("setup-error").textContent = data.error || "Could not load questions.";
                document.getElementById("setup-error").classList.remove("hidden");
                return;
            }
            state.questions = data.questions;
            state.currentIndex = 0;
            state.score = 0;
            state.totalPossible = state.questions.reduce((sum, q) => sum + q.points, 0);
            showScreen("quiz");
            renderQuestion();
        })
        .catch(() => showError("Connection error - try again"));
}

function renderQuestion() {
    const q = state.questions[state.currentIndex];
    document.getElementById("hud-score").textContent = "SCORE: " + padScore(state.score);
    document.getElementById("hud-counter").textContent =
        `Q ${state.currentIndex + 1}/${state.questions.length}`;

    document.getElementById("quiz-question").textContent = q.question;
    document.getElementById("quiz-hint").textContent = q.hint ? "HINT: " + q.hint : "";
    document.getElementById("quiz-feedback").classList.add("hidden");

    const isMulti = q.correct.length > 1;
    const optsEl = document.getElementById("quiz-options");
    optsEl.innerHTML = "";

    q.options.forEach(opt => {
        const btn = document.createElement("button");
        btn.textContent = opt;
        btn.dataset.letter = opt.charAt(0); // "a)", "b)", etc.
        btn.onclick = () => handleOptionClick(btn, isMulti);
        optsEl.appendChild(btn);
    });

    if (isMulti) {
        const submitBtn = document.createElement("button");
        submitBtn.textContent = "SUBMIT ANSWER";
        submitBtn.style.marginTop = "15px";
        submitBtn.onclick = () => checkAnswer(isMulti);
        submitBtn.id = "submit-multi";
        optsEl.appendChild(submitBtn);
    }

    // Timer
    const timerEl = document.getElementById("hud-timer");
    if (state.timed) {
        timerEl.classList.remove("hidden");
        startTimer();
    } else {
        timerEl.classList.add("hidden");
    }
}

function handleOptionClick(btn, isMulti) {
    if (isMulti) {
        btn.classList.toggle("selected");
    } else {
        document.querySelectorAll("#quiz-options button").forEach(b => b.classList.remove("selected"));
        btn.classList.add("selected");
        checkAnswer(false);
    }
}

function getSelectedLetters() {
    return Array.from(document.querySelectorAll("#quiz-options button.selected"))
        .map(b => b.dataset.letter);
}

function checkAnswer(isMulti) {
    stopTimer();
    const q = state.questions[state.currentIndex];
    const selected = getSelectedLetters().sort();
    const correct = [...q.correct].sort();

    const isCorrect = selected.length === correct.length &&
        selected.every((l, i) => l === correct[i]);

    const optionButtons = document.querySelectorAll("#quiz-options button[data-letter]");
    optionButtons.forEach(b => {
        b.disabled = true;
        const letter = b.dataset.letter;
        if (q.correct.includes(letter)) {
            b.classList.add("correct");
        } else if (b.classList.contains("selected")) {
            b.classList.add("incorrect");
        }
    });

    const multiBtn = document.getElementById("submit-multi");
    if (multiBtn) multiBtn.disabled = true;

    if (isCorrect) {
        state.score += q.points;
    }

    const feedback = document.getElementById("quiz-feedback");
    feedback.textContent = (isCorrect ? "CORRECT! " : "INCORRECT. ") + (q.explanation || "");
    feedback.classList.remove("hidden");

    setTimeout(nextQuestion, 2500);
}

function nextQuestion() {
    state.currentIndex++;
    if (state.currentIndex >= state.questions.length) {
        finishQuiz();
    } else {
        renderQuestion();
    }
}

// ------------- Timer -------------

function startTimer() {
    state.timeLeft = 20;
    updateTimerDisplay();
    state.timer = setInterval(() => {
        state.timeLeft--;
        updateTimerDisplay();
        if (state.timeLeft <= 0) {
            stopTimer();
            checkAnswer(false);
        }
    }, 1000);
}

function stopTimer() {
    if (state.timer) {
        clearInterval(state.timer);
        state.timer = null;
    }
}

function updateTimerDisplay() {
    document.getElementById("timer-text").textContent = state.timeLeft;
    const ring = document.querySelector(".timer-ring");
    const circumference = 2 * Math.PI * 17;
    const offset = circumference * (1 - state.timeLeft / 20);
    ring.style.strokeDashoffset = offset;
    const timerEl = document.getElementById("hud-timer");
    if (state.timeLeft <= 5) {
        timerEl.classList.add("urgent");
    } else {
        timerEl.classList.remove("urgent");
    }
}

// ------------- Results -------------

function finishQuiz() {
    const payload = {
        score: state.score,
        total_possible: state.totalPossible,
        category: state.category,
        difficulty: state.difficulty,
        timed: state.timed,
    };

    fetch("/api/submit-score", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload),
    })
        .then(r => r.json())
        .then(data => {
            const pct = data.entry ? data.entry.percentage : 0;
            document.getElementById("final-score").textContent = state.score;
            document.getElementById("final-total").textContent = state.totalPossible;
            document.getElementById("final-percent").textContent = pct;

            const rankEl = document.getElementById("final-rank");
            if (data.rank) {
                rankEl.textContent = "LEADERBOARD RANK: #" + data.rank;
            } else {
                rankEl.textContent = "NOT ON LEADERBOARD";
            }

            // New personal best? Check history quickly.
            fetch("/api/history")
                .then(r => r.json())
                .then(h => {
                    const prior = (h.history || []).slice(1); // exclude just-saved
                    const best = prior.reduce((m, e) => Math.max(m, e.percentage), 0);
                    if (pct > best) {
                        document.getElementById("final-pb").classList.remove("hidden");
                    } else {
                        document.getElementById("final-pb").classList.add("hidden");
                    }
                });

            showScreen("results");
        })
        .catch(() => showError("Connection error - try again"));
}

function setupResults() {
    document.getElementById("btn-play-again").onclick = () => {
        resetSetup();
        showScreen("setup");
    };
    document.getElementById("btn-show-leaderboard").onclick = showLeaderboard;
    document.getElementById("btn-show-history").onclick = showHistory;
    document.querySelectorAll(".back-btn").forEach(b => {
        b.onclick = () => showScreen(b.dataset.back);
    });
}

function resetSetup() {
    state.category = null;
    state.difficulty = null;
    state.timed = null;
    document.querySelectorAll(".chip").forEach(c => c.classList.remove("selected"));
    document.getElementById("btn-begin").disabled = true;
    document.getElementById("setup-error").classList.add("hidden");
}

// ------------- Leaderboard -------------

function showLeaderboard() {
    fetch("/api/leaderboard")
        .then(r => r.json())
        .then(data => {
            const tbody = document.getElementById("leaderboard-body");
            tbody.innerHTML = "";
            data.entries.forEach((e, i) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${i + 1}</td>
                    <td>${escapeHtml(e.username)}</td>
                    <td>${e.score}/${e.total_possible} (${e.percentage}%)</td>
                    <td>${escapeHtml(e.category).toUpperCase()}</td>
                    <td>${escapeHtml(e.difficulty).toUpperCase()}</td>
                `;
                tbody.appendChild(row);
            });
            if (data.entries.length === 0) {
                tbody.innerHTML = `<tr><td colspan="5" style="text-align:center">NO SCORES YET</td></tr>`;
            }
            showScreen("leaderboard");
        })
        .catch(() => showError("Connection error - try again"));
}

// ------------- History -------------

function showHistory() {
    fetch("/api/history")
        .then(r => r.json())
        .then(data => {
            const list = document.getElementById("history-list");
            list.innerHTML = "";
            if (!data.history || data.history.length === 0) {
                list.innerHTML = "<p>NO HISTORY YET</p>";
            } else {
                data.history.forEach(e => {
                    const div = document.createElement("div");
                    div.className = "history-entry";
                    const date = e.timestamp.slice(0, 10);
                    const timedLabel = e.timed ? "TIMED" : "UNTIMED";
                    div.innerHTML = `<span class="date">${date}</span>` +
                        `${escapeHtml(e.category).toUpperCase()} / ${escapeHtml(e.difficulty).toUpperCase()} / ${timedLabel} &middot; ` +
                        `${e.score}/${e.total_possible} (${e.percentage}%)`;
                    list.appendChild(div);
                });
            }
            showScreen("history");
        })
        .catch(() => showError("Connection error - try again"));
}

// ------------- Utilities -------------

function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;"
    })[c]);
}

// ------------- Init -------------

window.addEventListener("DOMContentLoaded", () => {
    setupWelcome();
    setupSetup();
    setupResults();
    showScreen("welcome");
});
