# question_creator.py
# ITM352 - Spring 2026 - Assignment 1
# Justin
#
# Separate app for adding questions to the quiz database (requirement 8).
# Run this instead of main.py when you want to create new questions --
# it walks you through entering the question text, options, correct answers,
# a hint, and an explanation, then saves everything to questions.json in
# the right format.
#
# Run with: python question_creator.py

import json
import os

# Same questions file the main quiz uses
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "data", "questions.json")


# ----------------------------------------------------------------
# File I/O
# ----------------------------------------------------------------

def load_data():
    """
    Loads the existing questions from the JSON file. If it doesn't exist
    yet we just return an empty structure -- the first question you add
    will create the file.
    """
    if not os.path.exists(QUESTIONS_FILE):
        return {"categories": {}}
    try:
        with open(QUESTIONS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: couldn't read the questions file, starting fresh.")
        return {"categories": {}}


def save_data(data):
    """Writes the questions data back to questions.json."""
    os.makedirs(os.path.dirname(QUESTIONS_FILE), exist_ok=True)
    with open(QUESTIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\n  Saved to {QUESTIONS_FILE}")


# ----------------------------------------------------------------
# Category helpers
# ----------------------------------------------------------------

def pick_or_create_category(data):
    """
    Shows the existing categories and lets the user pick one or make a new one.
    Keeps re-prompting if they type something that isn't a valid number.
    """
    categories = list(data["categories"].keys())

    print("\n  Existing categories:")
    for i, cat in enumerate(categories, start=1):
        count = len(data["categories"][cat])
        print(f"    {i}. {cat.title()}  ({count} question(s))")
    print(f"    {len(categories) + 1}. Create a new category")

    while True:
        choice = input("\n  Your choice: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(categories):
                return categories[idx]
            elif idx == len(categories):
                return _create_category(data)
        print("  Please enter a valid number.")


def _create_category(data):
    """Prompts for a new category name and adds it to the data dict."""
    while True:
        name = input("  New category name: ").strip().lower()
        if name:
            if name in data["categories"]:
                print(f"  '{name}' already exists, switching to it.")
            else:
                data["categories"][name] = []
                print(f"  Category '{name}' created.")
            return name
        print("  Category name can't be empty.")


# ----------------------------------------------------------------
# Question builder
# ----------------------------------------------------------------

def build_question():
    """
    Walks the user through entering all the parts of a question interactively.
    Requires at least 4 options, up to 6. Returns a dict that matches the
    format questions.json expects.
    """
    print("\n  --- New Question ---")

    # Get the question text -- can't be empty
    question_text = ""
    while not question_text:
        question_text = input("  Question text: ").strip()
        if not question_text:
            print("  Question text can't be empty.")

    # Collect options a-f, first 4 are required
    letters = ["a", "b", "c", "d", "e", "f"]
    options = []

    print("\n  Enter the answer options (first 4 are required).")
    for letter in letters:
        required = len(options) < 4
        prompt = f"  Option {letter}{'*' if required else ' (optional -- press Enter to stop)'}: "
        while True:
            text = input(prompt).strip()
            if text:
                options.append(f"{letter}) {text}")
                break
            elif not required:
                # They pressed Enter on an optional one, we're done collecting
                return _finish_question(question_text, options)
            else:
                print(f"  Option {letter} is required.")

    return _finish_question(question_text, options)


def _finish_question(question_text, options):
    """
    Collects the correct answer(s), hint, and explanation after we have
    all the options. Split into its own function because build_question()
    can return early (when the user skips an optional option) and both
    code paths need to finish the same way.
    """
    valid_letters = [opt[0] for opt in options]
    valid_str = ", ".join(valid_letters)

    print(f"\n  Available options: {valid_str}")
    print("  Enter the correct answer letter(s), separated by commas (e.g. 'c' or 'a,c,d'):")

    correct = []
    while not correct:
        raw = input("  Correct answer(s): ").strip().lower()
        # Support "a,c" or "a c" or "ac" -- normalize and split into individual letters
        parsed = [c.strip() for c in raw.replace(",", " ").split() if c.strip()]
        if parsed and all(c in valid_letters for c in parsed) and len(parsed) == len(set(parsed)):
            correct = parsed
        else:
            print(f"  Invalid. Enter one or more of: {valid_str}  (no duplicates)")

    hint = input("\n  Hint (optional -- press Enter to skip): ").strip()
    explanation = input("  Explanation (why is this the correct answer?): ").strip()

    return {
        "question": question_text,
        "options": options,
        "correct": correct,
        "hint": hint,
        "explanation": explanation
    }


# ----------------------------------------------------------------
# View helper
# ----------------------------------------------------------------

def view_category(data):
    """Prints all questions in a chosen category with correct answers marked."""
    if not data["categories"]:
        print("\n  No categories yet.")
        return

    category = pick_or_create_category(data)
    questions = data["categories"].get(category, [])

    if not questions:
        print(f"\n  No questions in '{category}' yet.")
        return

    print(f"\n  --- {category.title()} ({len(questions)} question(s)) ---")
    for i, q in enumerate(questions, start=1):
        print(f"\n  {i}. {q['question']}")
        for opt in q["options"]:
            # Put a checkmark next to correct answers so they're easy to spot
            marker = "✓" if opt[0] in q["correct"] else " "
            print(f"     [{marker}] {opt}")
        if q.get("hint"):
            print(f"       Hint: {q['hint']}")
        if q.get("explanation"):
            print(f"       Explanation: {q['explanation']}")


# ----------------------------------------------------------------
# Main menu
# ----------------------------------------------------------------

def main():
    """Simple menu loop -- add questions, view them, or save and exit."""
    print("=" * 50)
    print("     QUIZ QUESTION CREATOR")
    print("     ITM352 — Spring 2026")
    print("=" * 50)
    print("Add new questions to the quiz database.")

    data = load_data()
    unsaved_changes = False

    while True:
        print("\n" + "-" * 30)
        print("  1. Add a new question")
        print("  2. View questions in a category")
        print("  3. Save and exit")
        print("  4. Exit without saving")

        choice = input("\n  Choice: ").strip()

        if choice == "1":
            category = pick_or_create_category(data)
            question = build_question()
            data["categories"][category].append(question)
            unsaved_changes = True
            print(f"\n  Question added to '{category.title()}'!")

        elif choice == "2":
            view_category(data)

        elif choice == "3":
            save_data(data)
            print("  Goodbye!")
            break

        elif choice == "4":
            if unsaved_changes:
                confirm = input("  You have unsaved changes. Really exit? (y/n): ").strip().lower()
                if confirm != "y":
                    continue
            print("  Exiting without saving. Goodbye!")
            break

        else:
            print("  Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
