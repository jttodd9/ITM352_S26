# src/quiz.py
# ============================================================
# Quiz Module - ITM352 Spring 2026 - Assignment 1
#
# Core quiz logic. Manages the full game flow:
#   - User login (extra credit: per-user high scores, grand champion)
#   - Category selection (requirement 5)
#   - Per-question: timer with bonus points (req 9), hints (req 6),
#     50/50 lifeline (req 10), multiple correct answers (req 3/4),
#     explanations (req 7)
#   - Score history saved to file (req 1)
#   - New high score notification (req 2)
# ============================================================

import json
import os
import time

from src.scoring import load_scores, save_score, get_grand_champion
from src.utils import get_valid_input, clear_screen, display_banner


class Quiz:
    """
    Main quiz class that orchestrates the entire game.

    Attributes:
        username (str):          The logged-in player's name.
        score (int):             Number of questions answered correctly.
        bonus_score (int):       Bonus points earned for fast answers.
        questions (list):        Questions for the chosen category.
        category (str):          The chosen category name.
        fifty_fifty_used (bool): Whether the 50/50 lifeline has been used.
    """

    # Path to the questions JSON file (relative to this file's location)
    QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "questions.json")

    # Timer settings
    BONUS_THRESHOLD = 10   # seconds; answer faster than this to earn a bonus point
    BONUS_POINTS = 1       # bonus points awarded for a fast correct answer

    def __init__(self):
        self.username = ""
        self.score = 0
        self.bonus_score = 0
        self.questions = []
        self.category = ""
        self.fifty_fifty_used = False
        self.questions_data = self._load_questions()

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self):
        """Start the full quiz: banner → login → category → questions → results."""
        display_banner()
        self._login()
        self._select_category()
        self._run_quiz()
        self._show_results()

    # ------------------------------------------------------------------
    # Setup helpers
    # ------------------------------------------------------------------

    def _load_questions(self):
        """
        Load and return the questions dictionary from the JSON data file.

        Returns:
            dict: Full JSON contents, or {"categories": {}} on error.
        """
        try:
            with open(self.QUESTIONS_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Questions file not found at {self.QUESTIONS_FILE}")
            return {"categories": {}}
        except json.JSONDecodeError:
            print("Error: The questions file contains invalid JSON.")
            return {"categories": {}}

    def _login(self):
        """
        Prompt for a username, then display the player's personal best
        and the current grand champion (extra credit).
        """
        print("\n" + "=" * 50)
        print("Enter your name to log in (or press Enter to play as 'guest'):")
        name = input("> ").strip()
        self.username = name if name else "guest"

        print(f"\nWelcome, {self.username}!")

        # Show personal best and grand champion if records exist
        scores = load_scores()
        if self.username in scores["users"]:
            personal_best = scores["users"][self.username]["high_score"]
            print(f"  Your personal best: {personal_best} points")

        champion = get_grand_champion(scores)
        if champion:
            print(f"  Grand Champion:     {champion['name']} — {champion['score']} points")

    def _select_category(self):
        """
        Display available quiz categories and let the player choose one.
        Validates input so only a valid number is accepted.
        """
        categories = list(self.questions_data["categories"].keys())

        print("\n" + "=" * 50)
        print("Available Categories:")
        for i, cat in enumerate(categories, start=1):
            q_count = len(self.questions_data["categories"][cat])
            print(f"  {i}. {cat.title()}  ({q_count} questions)")

        valid_nums = [str(i) for i in range(1, len(categories) + 1)]
        choice = get_valid_input(f"\nSelect a category (1-{len(categories)}): ", valid_nums)
        self.category = categories[int(choice) - 1]
        self.questions = self.questions_data["categories"][self.category]

        print(f"\nCategory: {self.category.title()}")
        print(f"Questions: {len(self.questions)}\n")
        print("How to play:")
        print("  Enter a letter  →  answer (e.g. 'b')")
        print("  Enter letters   →  multi-answer (e.g. 'a,c' or 'acd')")
        print("  Type 'hint'     →  get a hint (if available)")
        print("  Type '5050'     →  use your 50/50 lifeline (once per game)")
        print(f"  Answer within {self.BONUS_THRESHOLD}s →  earn +{self.BONUS_POINTS} bonus point!")
        input("\nPress Enter to begin...")

    # ------------------------------------------------------------------
    # Quiz loop
    # ------------------------------------------------------------------

    def _run_quiz(self):
        """Iterate through every question in the selected category."""
        self.score = 0
        self.bonus_score = 0
        self.fifty_fifty_used = False

        for idx, question_data in enumerate(self.questions):
            clear_screen()
            running_total = self.score + self.bonus_score
            print(f"\n--- Question {idx + 1} of {len(self.questions)} "
                  f"| Score: {running_total} ---")
            self._ask_question(question_data)
            print()  # spacing before next question

    def _ask_question(self, question_data):
        """
        Present one question and handle all user interaction until a valid
        answer is submitted.

        Supports:
          - Hint requests (req 6)
          - 50/50 lifeline (req 10)
          - Single or multiple correct answers (req 3 & 4)
          - Per-answer timing with speed bonus (req 9)
          - Explanation after answer (req 7)

        Args:
            question_data (dict): One question entry from the JSON file.
                Expected keys: question, options, correct, hint, explanation
        """
        correct_answers = question_data["correct"]   # e.g. ["c"] or ["a","c","d"]
        is_multi = len(correct_answers) > 1

        print(f"\n{question_data['question']}")
        if is_multi:
            print("  (Multiple correct answers — select ALL that apply, e.g. 'a,c')")

        # Work with a mutable copy of options so 50/50 can mark eliminations
        options = list(question_data["options"])
        eliminated = set()   # letters eliminated by 50/50

        start_time = time.time()   # start timing as soon as question is shown

        while True:
            # --- Display options (skip eliminated ones) ---
            print()
            for opt in options:
                letter = opt[0].lower()
                if letter not in eliminated:
                    print(f"  {opt}")

            # --- Show available special commands ---
            specials = []
            if question_data.get("hint") and not eliminated:
                specials.append("'hint'")
            if not self.fifty_fifty_used and not eliminated:
                specials.append("'5050'")
            if specials:
                print(f"  [Commands: {', '.join(specials)}]")

            user_input = input("\nYour answer: ").strip().lower()

            # --- Handle hint ---
            if user_input == "hint":
                hint_text = question_data.get("hint", "")
                if hint_text:
                    print(f"\n  Hint: {hint_text}")
                else:
                    print("\n  No hint available for this question.")
                continue

            # --- Handle 50/50 ---
            if user_input == "5050":
                if self.fifty_fifty_used:
                    print("\n  You have already used your 50/50 lifeline this game!")
                    continue
                eliminated = self._apply_fifty_fifty(options, correct_answers)
                self.fifty_fifty_used = True
                print("\n  50/50 used! Two wrong answers have been eliminated.")
                continue

            # --- Parse the answer into a list of letters ---
            parsed = self._parse_answer(user_input)

            # --- Validate against available (non-eliminated) options ---
            available = {opt[0].lower() for opt in options if opt[0].lower() not in eliminated}
            if not parsed or not all(letter in available for letter in parsed):
                print(f"\n  Invalid input. Please enter letter(s) from: "
                      f"{', '.join(sorted(available))}")
                continue

            # Check for duplicates
            if len(parsed) != len(set(parsed)):
                print("\n  Duplicate entries detected — enter each letter only once.")
                continue

            # --- Valid answer received — stop the clock ---
            elapsed = time.time() - start_time

            # --- Check correctness ---
            is_correct = sorted(parsed) == sorted(correct_answers)

            if is_correct:
                print("\n  Correct!")
                self.score += 1
                if elapsed <= self.BONUS_THRESHOLD:
                    self.bonus_score += self.BONUS_POINTS
                    print(f"  Speed bonus! Answered in {elapsed:.1f}s "
                          f"(+{self.BONUS_POINTS} bonus point)")
            else:
                correct_str = ", ".join(correct_answers).upper()
                print(f"\n  Incorrect. Correct answer(s): {correct_str}")

            print(f"  Time taken: {elapsed:.1f}s")

            # --- Always show explanation ---
            explanation = question_data.get("explanation", "")
            if explanation:
                print(f"\n  Explanation: {explanation}")

            break   # move to next question

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    def _parse_answer(self, raw):
        """
        Parse a raw answer string into a list of individual lowercase letters.

        Accepts formats: 'b', 'a,c', 'a, c', 'acd', 'a c'.

        Args:
            raw (str): The user's raw input string.

        Returns:
            list[str]: List of single lowercase letters, or [] if invalid.
        """
        # Normalise: strip commas and spaces, split into characters
        cleaned = raw.replace(",", "").replace(" ", "")
        letters = list(cleaned)
        if letters and all(c.isalpha() for c in letters):
            return letters
        return []

    def _apply_fifty_fifty(self, options, correct_answers):
        """
        Choose two wrong-answer letters to eliminate for the 50/50 lifeline.

        Args:
            options (list[str]):        All option strings (e.g. "a) Rome").
            correct_answers (list[str]): Letters of correct answers.

        Returns:
            set[str]: The two (or fewer) wrong letters to eliminate.
        """
        wrong = [opt[0].lower() for opt in options
                 if opt[0].lower() not in correct_answers]
        return set(wrong[:2])   # eliminate up to two wrong answers

    # ------------------------------------------------------------------
    # Results
    # ------------------------------------------------------------------

    def _show_results(self):
        """
        Display the final score, check for a new personal high score,
        save results to the scores file, and show the grand champion.
        """
        total = self.score + self.bonus_score
        num_q = len(self.questions)
        percentage = (self.score / num_q * 100) if num_q else 0

        clear_screen()
        print("\n" + "=" * 50)
        print("  QUIZ COMPLETE!")
        print("=" * 50)
        print(f"  Player:       {self.username}")
        print(f"  Category:     {self.category.title()}")
        print(f"  Base Score:   {self.score} / {num_q}  ({percentage:.0f}%)")
        print(f"  Bonus Points: {self.bonus_score}")
        print(f"  TOTAL:        {total}")
        print("=" * 50)

        # Performance message
        if percentage == 100:
            print("  Perfect score! Outstanding!")
        elif percentage >= 70:
            print("  Great job!")
        elif percentage >= 50:
            print("  Not bad — keep studying!")
        else:
            print("  Better luck next time!")

        # Save score and check for new personal high score (req 1 & 2)
        scores = load_scores()
        is_new_high = save_score(scores, self.username, self.category, total)

        if is_new_high:
            print(f"\n  *** NEW PERSONAL HIGH SCORE for {self.username}! ***")

        # Show updated grand champion (extra credit)
        champion = get_grand_champion(load_scores())   # reload after save
        if champion:
            print(f"\n  Grand Champion: {champion['name']} — {champion['score']} points")

        print("\nThanks for playing!\n")
