# ============================================================
# Interactive Quiz Application
# ITM352 - Spring 2026 - Assignment 1
# 
# This program loads quiz questions from a JSON file,
# lets the user choose a category, asks multiple-choice
# questions, validates input, and reports a final score.
# ============================================================

import json
import os

# ---- Configuration ----
# Path to the questions file (relative to this script's location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(SCRIPT_DIR, "data", "questions.json")


def load_questions(filepath):
    """
    Load quiz questions from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file containing questions.
    
    Returns:
        dict: A dictionary with category names as keys and 
              lists of question dicts as values.
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return data["categories"]


def choose_category(categories):
    """
    Display available categories and let the user pick one.
    Validates that the user enters a valid choice.
    
    Args:
        categories (dict): Dictionary of category_name -> question_list.
    
    Returns:
        str: The chosen category name.
    """
    category_names = list(categories.keys())

    print("\n===== Choose a Category =====")
    for i, name in enumerate(category_names, start=1):
        # Show category name capitalized and how many questions it has
        print(f"  {i}) {name.capitalize()} ({len(categories[name])} questions)")

    # Keep prompting until we get a valid number
    while True:
        choice = input(f"\nEnter your choice (1-{len(category_names)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(category_names):
            selected = category_names[int(choice) - 1]
            print(f"\nYou selected: {selected.capitalize()}")
            return selected
        else:
            print(f"Invalid choice. Please enter a number between 1 and {len(category_names)}.")


def ask_question(question_data, question_number):
    """
    Present a single question to the user, validate their input,
    and determine if they answered correctly. This is the main
    non-trivial custom function — it handles:
      - Displaying the question and options
      - Offering a hint (optional)
      - Accepting single or multiple answers
      - Validating input against allowed option letters
      - Checking correctness and showing the explanation
    
    Args:
        question_data (dict): A single question dict from the JSON file.
        question_number (int): The question number (for display).
    
    Returns:
        bool: True if the user answered correctly, False otherwise.
    """
    question_text = question_data["question"]
    options = question_data["options"]
    correct_answers = question_data["correct"]  # list, e.g. ["b"] or ["a", "c", "d"]
    hint = question_data["hint"]
    explanation = question_data["explanation"]

    # Build the set of valid option letters from the options list
    # e.g. ["a) ...", "b) ...", "c) ...", "d) ..."] -> {"a", "b", "c", "d"}
    valid_letters = set()
    for opt in options:
        letter = opt.strip()[0].lower()  # grab first character
        valid_letters.add(letter)

    # Determine if this is a multi-answer question
    is_multi = len(correct_answers) > 1

    # Display the question
    print(f"\n--- Question {question_number} ---")
    print(question_text)
    if is_multi:
        print("  (This question has MULTIPLE correct answers. Enter all that apply, e.g. 'a,c,d')")
    print()
    for opt in options:
        print(f"  {opt}")

    # Prompt loop: get valid input from user
    while True:
        # Offer hint option
        user_input = input("\nYour answer (or type 'hint' for a hint): ").strip().lower()

        # Handle hint request
        if user_input == "hint":
            print(f"  HINT: {hint}")
            continue  # re-prompt after showing hint

        # Parse the answer(s) — support both "b" and "a,c,d" formats
        # Remove spaces and split by comma
        user_answers = [a.strip() for a in user_input.split(",") if a.strip()]

        # Validate: every answer must be a valid option letter
        if not user_answers:
            print(f"Please enter a valid option ({', '.join(sorted(valid_letters))}).")
            continue

        all_valid = all(a in valid_letters for a in user_answers)
        if not all_valid:
            print(f"Invalid input. Valid options are: {', '.join(sorted(valid_letters))}.")
            continue

        # Check for duplicate entries
        if len(user_answers) != len(set(user_answers)):
            print("Duplicate answers detected. Please enter each option only once.")
            continue

        # We have valid input — now check correctness
        # Sort both lists so order doesn't matter
        is_correct = sorted(user_answers) == sorted(correct_answers)

        if is_correct:
            print("  ✓ Correct!")
        else:
            correct_display = ", ".join(correct_answers)
            print(f"  ✗ Incorrect. The correct answer(s): {correct_display}")

        # Always show explanation
        print(f"  Explanation: {explanation}")

        return is_correct


def run_quiz():
    """
    Main function that orchestrates the quiz:
    1. Load questions from file
    2. Let user choose a category
    3. Ask each question
    4. Report the final score
    """
    print("=" * 50)
    print("   Welcome to the Interactive Quiz App!")
    print("=" * 50)

    # Step 1: Load questions
    try:
        categories = load_questions(QUESTIONS_FILE)
    except FileNotFoundError:
        print(f"Error: Questions file not found at {QUESTIONS_FILE}")
        print("Make sure the 'data/questions.json' file exists.")
        return
    except json.JSONDecodeError:
        print("Error: The questions file contains invalid JSON.")
        return

    # Step 2: Choose a category
    category = choose_category(categories)
    questions = categories[category]

    # Step 3: Ask each question and track the score
    score = 0
    total = len(questions)

    for i, q in enumerate(questions, start=1):
        if ask_question(q, i):
            score += 1

    # Step 4: Report the final score
    print("\n" + "=" * 50)
    print(f"   Quiz Complete!")
    print(f"   Your Score: {score} / {total}")
    percentage = (score / total) * 100 if total > 0 else 0
    print(f"   Percentage: {percentage:.0f}%")
    print("=" * 50)

    # Give feedback based on score
    if percentage == 100:
        print("   Perfect score! Amazing!")
    elif percentage >= 70:
        print("   Great job!")
    elif percentage >= 50:
        print("   Not bad, keep studying!")
    else:
        print("   Better luck next time!")


# ---- Entry Point ----
if __name__ == "__main__":
    run_quiz()
