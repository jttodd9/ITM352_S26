# question_creator.py
# ============================================================
# Question Creator Application — Requirement 8
# ITM352 Spring 2026 - Assignment 1
#
# A standalone interactive tool that lets you build new quiz
# questions and save them to the questions.json file in the
# correct format.
#
# Run with:  python question_creator.py
# ============================================================

import json
import os

# Path to the shared questions file
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "data", "questions.json")


# ------------------------------------------------------------------
# File I/O helpers
# ------------------------------------------------------------------

def load_data():
    """
    Load the existing questions from the JSON file.

    Returns:
        dict: The questions data, or a blank structure if not found.
    """
    if not os.path.exists(QUESTIONS_FILE):
        return {"categories": {}}
    try:
        with open(QUESTIONS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read questions file — starting fresh.")
        return {"categories": {}}


def save_data(data):
    """
    Write the questions data back to the JSON file.

    Args:
        data (dict): The full questions dictionary.
    """
    os.makedirs(os.path.dirname(QUESTIONS_FILE), exist_ok=True)
    with open(QUESTIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\n  Saved to {QUESTIONS_FILE}")


# ------------------------------------------------------------------
# Category helpers
# ------------------------------------------------------------------

def pick_or_create_category(data):
    """
    Show existing categories and let the user pick one or create a new one.

    Args:
        data (dict): The full questions dictionary.

    Returns:
        str: The chosen category key (lowercase).
    """
    categories = list(data["categories"].keys())

    print("\n  Existing categories:")
    for i, cat in enumerate(categories, start=1):
        count = len(data["categories"][cat])
        print(f"    {i}. {cat.title()}  ({count} question(s))")
    print(f"    {len(categories) + 1}. + Create a new category")

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
    """Prompt for a new category name and initialise it in data."""
    while True:
        name = input("  New category name: ").strip().lower()
        if name:
            if name in data["categories"]:
                print(f"  '{name}' already exists — switching to it.")
            else:
                data["categories"][name] = []
                print(f"  Category '{name}' created.")
            return name
        print("  Category name cannot be empty.")


# ------------------------------------------------------------------
# Question builder
# ------------------------------------------------------------------

def build_question():
    """
    Interactively collect all data for one quiz question.

    Returns:
        dict: A question dict ready to append to a category list.
    """
    print("\n  --- New Question ---")

    question_text = ""
    while not question_text:
        question_text = input("  Question text: ").strip()
        if not question_text:
            print("  Question text cannot be empty.")

    # Collect answer options (at least 4, up to 6)
    letters = ["a", "b", "c", "d", "e", "f"]
    options = []

    print("\n  Enter answer options (minimum 4 required).")
    for letter in letters:
        required = len(options) < 4
        prompt = f"  Option {letter}{'*' if required else ' (optional, Enter to stop)'}: "
        while True:
            text = input(prompt).strip()
            if text:
                options.append(f"{letter}) {text}")
                break
            elif not required:
                # Optional option skipped — stop collecting
                return _finish_question(question_text, options)
            else:
                print(f"  Option {letter} is required.")

    return _finish_question(question_text, options)


def _finish_question(question_text, options):
    """
    Collect correct answers, hint, and explanation for a question.

    Args:
        question_text (str): The question string.
        options (list[str]):  The answer option strings.

    Returns:
        dict: Complete question dict.
    """
    valid_letters = [opt[0] for opt in options]
    valid_str = ", ".join(valid_letters)

    print(f"\n  Available options: {valid_str}")
    print("  Enter the correct answer letter(s), comma-separated (e.g. 'c' or 'a,c,d'):")

    correct = []
    while not correct:
        raw = input("  Correct answer(s): ").strip().lower()
        # Parse comma- or space-separated letters
        parsed = [c.strip() for c in raw.replace(",", " ").split() if c.strip()]
        if parsed and all(c in valid_letters for c in parsed) and len(parsed) == len(set(parsed)):
            correct = parsed
        else:
            print(f"  Invalid. Enter one or more letters from: {valid_str} (no duplicates).")

    hint = input("\n  Hint (optional, press Enter to skip): ").strip()
    explanation = input("  Explanation (why is the answer correct?): ").strip()

    return {
        "question": question_text,
        "options": options,
        "correct": correct,
        "hint": hint,
        "explanation": explanation
    }


# ------------------------------------------------------------------
# View helpers
# ------------------------------------------------------------------

def view_category(data):
    """Display all questions in a chosen category."""
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
            marker = "✓" if opt[0] in q["correct"] else " "
            print(f"     [{marker}] {opt}")
        if q.get("hint"):
            print(f"       Hint: {q['hint']}")
        if q.get("explanation"):
            print(f"       Explanation: {q['explanation']}")


# ------------------------------------------------------------------
# Main loop
# ------------------------------------------------------------------

def main():
    """Main menu loop for the question creator application."""
    print("=" * 50)
    print("     QUIZ QUESTION CREATOR")
    print("     ITM352 — Spring 2026")
    print("=" * 50)
    print("Use this tool to add questions to the quiz database.")

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
