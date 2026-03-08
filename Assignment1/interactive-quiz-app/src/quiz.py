# src/quiz.py
# ITM352 - Spring 2026 - Assignment 1
# Justin
#
# This is the main Quiz class. It handles everything that happens
# during a game: loading questions, login, picking a category,
# running through each question, and showing the final score.
#
# Features handled here:
#   - User login and personal high scores (extra credit)
#   - Category selection (req 5)
#   - Hints during questions (req 6)
#   - 50/50 lifeline -- eliminates two wrong answers, once per game (req 10)
#   - Multiple correct answers and flexible input parsing (req 3 & 4)
#   - Per-question timer with speed bonus points (req 9)
#   - Explanations shown after every answer (req 7)
#   - Score saved to file and high score check at the end (req 1 & 2)

import json
import os
import time

from src.scoring import load_scores, save_score, get_grand_champion
from src.utils import get_valid_input, clear_screen, display_banner


class Quiz:
    """
    Handles the full quiz from start to finish.

    I put everything in one class to keep related stuff together -- login,
    category picking, question loop, and results. The scoring/file stuff
    lives in scoring.py so this file doesn't get too long.
    """

    # Using os.path.join so the file path works no matter where you run the script from
    QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "questions.json")

    # Answer within 10 seconds to earn a bonus point
    BONUS_THRESHOLD = 10
    BONUS_POINTS = 1

    def __init__(self):
        self.username = ""
        self.score = 0
        self.bonus_score = 0
        self.questions = []
        self.category = ""
        self.fifty_fifty_used = False  # only gets one use per game
        self.questions_data = self._load_questions()

    def run(self):
        # Main flow -- each step leads into the next
        display_banner()
        self._login()
        self._select_category()
        self._run_quiz()
        self._show_results()

    # ----------------------------------------------------------------
    # Loading questions
    # ----------------------------------------------------------------

    def _load_questions(self):
        """
        Reads questions.json and returns it as a dict. If the file is
        missing or has bad JSON, we return an empty structure instead of
        crashing so the error message is actually readable.
        """
        try:
            with open(self.QUESTIONS_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Couldn't find the questions file at: {self.QUESTIONS_FILE}")
            return {"categories": {}}
        except json.JSONDecodeError:
            print("The questions file has a formatting error -- check the JSON and try again.")
            return {"categories": {}}

    # ----------------------------------------------------------------
    # Login (extra credit)
    # ----------------------------------------------------------------

    def _login(self):
        """
        Asks for a username so we can track scores per player.
        Pressing Enter defaults to 'guest'. Shows your personal best
        and the current grand champion if either one exists.
        """
        print("\n" + "=" * 50)
        print("Enter your name to log in, or press Enter to play as guest:")
        name = input("> ").strip()
        self.username = name if name else "guest"

        print(f"\nWelcome, {self.username}!")

        # Show their previous high score if they've played before
        scores = load_scores()
        if self.username in scores["users"]:
            personal_best = scores["users"][self.username]["high_score"]
            print(f"  Your personal best: {personal_best} points")

        # Show the grand champion so there's something to beat
        champion = get_grand_champion(scores)
        if champion:
            print(f"  Grand Champion:     {champion['name']} — {champion['score']} points")

    # ----------------------------------------------------------------
    # Category selection (req 5)
    # ----------------------------------------------------------------

    def _select_category(self):
        """
        Reads the categories out of the JSON and lets the player pick one.
        get_valid_input() handles re-prompting if they type something invalid.
        """
        categories = list(self.questions_data["categories"].keys())

        print("\n" + "=" * 50)
        print("Pick a category:")
        for i, cat in enumerate(categories, start=1):
            q_count = len(self.questions_data["categories"][cat])
            print(f"  {i}. {cat.title()}  ({q_count} questions)")

        valid_nums = [str(i) for i in range(1, len(categories) + 1)]
        choice = get_valid_input(f"\nEnter a number (1-{len(categories)}): ", valid_nums)
        self.category = categories[int(choice) - 1]
        self.questions = self.questions_data["categories"][self.category]

        print(f"\nAlright, {self.category.title()} it is!")
        print(f"{len(self.questions)} questions coming up.\n")
        print("How it works:")
        print("  Type a letter to answer            (e.g. 'b')")
        print("  Separate letters for multi-answer  (e.g. 'a,c' or 'acd')")
        print("  Type 'hint' for a hint             (if one is available)")
        print("  Type '5050' to eliminate 2 wrong answers  (once per game)")
        print(f"  Answer in under {self.BONUS_THRESHOLD}s to earn a +{self.BONUS_POINTS} speed bonus!")
        input("\nPress Enter when you're ready...")

    # ----------------------------------------------------------------
    # Main question loop
    # ----------------------------------------------------------------

    def _run_quiz(self):
        """Loops through each question and calls _ask_question() for each one."""
        self.score = 0
        self.bonus_score = 0
        self.fifty_fifty_used = False

        for idx, question_data in enumerate(self.questions):
            clear_screen()
            running_total = self.score + self.bonus_score
            print(f"\n--- Question {idx + 1} of {len(self.questions)} "
                  f"| Score: {running_total} ---")
            self._ask_question(question_data)
            print()

    def _ask_question(self, question_data):
        """
        Shows one question and keeps looping until the player gives a valid answer.

        This function is doing a lot -- hints, 50/50, multi-answer parsing,
        timing, correctness checking, and showing the explanation. I kept it
        in one function because all these pieces share the same state (the
        options list, the eliminated set, the timer) and splitting it up
        would have meant passing a lot of variables around.
        """
        correct_answers = question_data["correct"]  # list like ["b"] or ["a","c","d"]
        is_multi = len(correct_answers) > 1

        print(f"\n{question_data['question']}")
        if is_multi:
            # Let the player know upfront so they don't just enter one letter
            print("  (Multiple correct answers -- enter all of them, e.g. 'a,c')")

        # Copy the options list so 50/50 can mark eliminations
        # without messing with the original question data
        options = list(question_data["options"])
        eliminated = set()

        # Start timing as soon as the question is on screen
        start_time = time.time()

        while True:
            # Only show options that haven't been eliminated
            print()
            for opt in options:
                letter = opt[0].lower()
                if letter not in eliminated:
                    print(f"  {opt}")

            # Only show commands that are actually usable right now
            specials = []
            if question_data.get("hint") and not eliminated:
                specials.append("'hint'")
            if not self.fifty_fifty_used and not eliminated:
                specials.append("'5050'")
            if specials:
                print(f"  [Commands: {', '.join(specials)}]")

            user_input = input("\nYour answer: ").strip().lower()

            # Hint request (req 6)
            if user_input == "hint":
                hint_text = question_data.get("hint", "")
                if hint_text:
                    print(f"\n  Hint: {hint_text}")
                else:
                    print("\n  No hint available for this one.")
                continue

            # 50/50 lifeline (req 10)
            if user_input == "5050":
                if self.fifty_fifty_used:
                    print("\n  You already used 50/50 this game!")
                    continue
                eliminated = self._apply_fifty_fifty(options, correct_answers)
                self.fifty_fifty_used = True
                print("\n  50/50 used -- two wrong answers are gone.")
                continue

            # Parse whatever they typed into a list of letters (req 3)
            parsed = self._parse_answer(user_input)

            # Every letter has to be an available (non-eliminated) option
            available = {opt[0].lower() for opt in options if opt[0].lower() not in eliminated}
            if not parsed or not all(letter in available for letter in parsed):
                print(f"\n  Invalid input. Valid options right now: "
                      f"{', '.join(sorted(available))}")
                continue

            # Catch duplicate entries like "a,a"
            if len(parsed) != len(set(parsed)):
                print("\n  You entered the same letter more than once.")
                continue

            # Valid answer -- stop the timer
            elapsed = time.time() - start_time

            # Sort both lists so order doesn't matter (req 4)
            is_correct = sorted(parsed) == sorted(correct_answers)

            if is_correct:
                print("\n  Correct!")
                self.score += 1
                # Speed bonus if they answered fast enough (req 9)
                if elapsed <= self.BONUS_THRESHOLD:
                    self.bonus_score += self.BONUS_POINTS
                    print(f"  Speed bonus! Answered in {elapsed:.1f}s "
                          f"(+{self.BONUS_POINTS} bonus point)")
            else:
                correct_str = ", ".join(correct_answers).upper()
                print(f"\n  Not quite. Correct answer(s): {correct_str}")

            print(f"  Time: {elapsed:.1f}s")

            # Show the explanation whether they got it right or not (req 7)
            explanation = question_data.get("explanation", "")
            if explanation:
                print(f"\n  Explanation: {explanation}")

            break  # move to the next question

    # ----------------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------------

    def _parse_answer(self, raw):
        """
        Turns whatever the user typed into a clean list of letters.
        Handles "b", "a,c", "a, c", "acd", "a c" -- basically any
        reasonable way someone might type a multi-letter answer.
        Returns [] if there are non-letter characters in the input.
        """
        # Stripping commas and spaces means "a, c" and "ac" both end up as ['a','c']
        cleaned = raw.replace(",", "").replace(" ", "")
        letters = list(cleaned)
        if letters and all(c.isalpha() for c in letters):
            return letters
        return []

    def _apply_fifty_fifty(self, options, correct_answers):
        """
        Picks two wrong answers to eliminate for the 50/50 lifeline.
        Just grabs the first two wrong ones in the list -- simple and consistent.
        """
        wrong = [opt[0].lower() for opt in options
                 if opt[0].lower() not in correct_answers]
        return set(wrong[:2])

    # ----------------------------------------------------------------
    # Results (req 1 & 2)
    # ----------------------------------------------------------------

    def _show_results(self):
        """
        Shows the final score, saves it to the file, tells the player
        if they set a new personal best, and shows the grand champion.
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

        if percentage == 100:
            print("  Perfect score! Nice!")
        elif percentage >= 70:
            print("  Great job!")
        elif percentage >= 50:
            print("  Not bad, keep studying!")
        else:
            print("  Better luck next time!")

        # Save to the scores file and check if it's a new personal best
        scores = load_scores()
        is_new_high = save_score(scores, self.username, self.category, total)

        if is_new_high:
            print(f"\n  *** New personal high score for {self.username}! ***")

        # Reload after saving so we get the updated champion record
        champion = get_grand_champion(load_scores())
        if champion:
            print(f"\n  Grand Champion: {champion['name']} — {champion['score']} points")

        print("\nThanks for playing!\n")
