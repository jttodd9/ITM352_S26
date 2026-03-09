# question_creator.py
# ITM352 - Spring 2026 - Assignment 1
# Justin
#
# Separate app for adding quiz questions to the database (requirement 8).
# Run this when you want to add new questions.
# Run with: python question_creator.py

import json
import os

# Same questions file the main quiz reads from.
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "data", "questions.json")


# Loads questions.json and returns all the data inside.
# If the file doesn't exist yet, returns an empty starting structure.
def load_data():
    if not os.path.exists(QUESTIONS_FILE):
        return {"categories": {}}
    try:
        file = open(QUESTIONS_FILE, "r")
        data = json.load(file)
        file.close()
        return data
    except:
        # Something went wrong, start fresh rather than crash.
        print("Warning: couldn't read the file, starting fresh.")
        return {"categories": {}}


# Writes the data dictionary back to questions.json.
def save_data(data):
    os.makedirs(os.path.dirname(QUESTIONS_FILE), exist_ok=True)
    file = open(QUESTIONS_FILE, "w")
    json.dump(data, file, indent=4)
    file.close()
    print("\nSaved to " + QUESTIONS_FILE)


# Shows all existing categories and lets the user pick one or make a
# new one. Keeps looping until they enter a valid number.
# Returns the chosen category name as a lowercase string.
def pick_category(data):
    # Get the category names as an ordered list so we can number them.
    category_list = list(data["categories"].keys())

    print("\nExisting categories:")
    i = 1
    for cat in category_list:
        count = len(data["categories"][cat])
        print("  " + str(i) + ". " + cat.title() + "  (" + str(count) + " question(s))")
        i = i + 1

    # The last option is always "create new category".
    print("  " + str(len(category_list) + 1) + ". Create a new category")

    while True:
        choice = input("\nYour choice: ").strip()

        if choice.isdigit():
            idx = int(choice) - 1

            # They picked an existing category.
            if idx >= 0 and idx < len(category_list):
                return category_list[idx]

            # They picked the "create new" option.
            elif idx == len(category_list):
                while True:
                    new_name = input("New category name: ").strip().lower()
                    if new_name != "":
                        # Add it to the dict with an empty question list.
                        if new_name not in data["categories"]:
                            data["categories"][new_name] = []
                        return new_name
                    print("Name can't be empty.")

        print("Please enter a valid number.")


# Walks the user through entering all the parts of a new question
# interactively, then returns a dict formatted for questions.json.
# First 4 options are required, options e and f are optional.
def build_question():
    print("\n--- New Question ---")

    # Keep asking until they give us actual text.
    question_text = ""
    while question_text == "":
        question_text = input("Question text: ").strip()
        if question_text == "":
            print("Can't be empty.")

    # We'll go through letters a-f and stop when they skip one.
    letters = ["a", "b", "c", "d", "e", "f"]
    options = []

    print("\nEnter the answer options (first 4 are required).")
    for letter in letters:
        # The first 4 are required, the rest are optional.
        required = len(options) < 4

        if required:
            prompt = "Option " + letter + "*: "
        else:
            prompt = "Option " + letter + " (optional, press Enter to stop): "

        while True:
            text = input(prompt).strip()

            if text != "":
                options.append(letter + ") " + text)
                break
            elif not required:
                # They skipped an optional one, stop collecting options.
                break
            else:
                print("Option " + letter + " is required.")

        # Break out of the outer loop too if they skipped.
        if text == "" and not required:
            break

    # Pull the first letter from each option to know what's valid.
    valid_letters = []
    for opt in options:
        valid_letters.append(opt[0])

    print("\nAvailable options: " + ", ".join(valid_letters))
    print("Enter the correct answer letter(s) separated by commas (e.g. 'c' or 'a,c,d'):")

    # Keep asking until we have at least one valid, non-duplicate answer.
    correct = []
    while len(correct) == 0:
        raw = input("Correct answer(s): ").strip().lower()

        # Split by comma and clean up each piece.
        pieces = raw.split(",")
        parsed = []
        for piece in pieces:
            piece = piece.strip()
            if piece != "":
                parsed.append(piece)

        # Check every letter is actually one of the options.
        all_valid = True
        for letter in parsed:
            if letter not in valid_letters:
                all_valid = False

        # Check for duplicates by tracking what we've already seen.
        no_duplicates = True
        seen = []
        for letter in parsed:
            if letter in seen:
                no_duplicates = False
            seen.append(letter)

        if len(parsed) > 0 and all_valid and no_duplicates:
            correct = parsed
        else:
            print("Invalid. Enter one or more of: " + ", ".join(valid_letters) + " (no duplicates)")

    # Hint is optional, explanation is good to have but not required.
    hint = input("\nHint (optional, press Enter to skip): ").strip()
    explanation = input("Explanation (why is this correct?): ").strip()

    # Pack everything into a dict that matches the questions.json format.
    question = {
        "question": question_text,
        "options": options,
        "correct": correct,
        "hint": hint,
        "explanation": explanation
    }

    return question


# Prints every question in a chosen category with correct answers marked.
def view_questions(data):
    if len(data["categories"]) == 0:
        print("\nNo categories yet.")
        return

    category = pick_category(data)
    questions = data["categories"][category]

    if len(questions) == 0:
        print("\nNo questions in '" + category + "' yet.")
        return

    print("\n--- " + category.title() + " (" + str(len(questions)) + " question(s)) ---")

    i = 1
    for q in questions:
        print("\n" + str(i) + ". " + q["question"])
        for opt in q["options"]:
            # Show [CORRECT] next to any option that's a right answer.
            if opt[0] in q["correct"]:
                marker = "[CORRECT]"
            else:
                marker = "         "
            print("   " + marker + " " + opt)
        if q.get("hint") != "":
            print("   Hint: " + q.get("hint", ""))
        i = i + 1


# Main menu loop, runs until the user saves and exits or exits without saving.
def main():
    print("=" * 50)
    print("     QUIZ QUESTION CREATOR")
    print("     ITM352 - Spring 2026")
    print("=" * 50)

    data = load_data()

    # Track whether there are changes that haven't been written to disk yet.
    unsaved = False

    while True:
        print("\n" + "-" * 30)
        print("  1. Add a new question")
        print("  2. View questions in a category")
        print("  3. Save and exit")
        print("  4. Exit without saving")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            category = pick_category(data)
            question = build_question()
            data["categories"][category].append(question)
            unsaved = True
            print("\nQuestion added to '" + category.title() + "'!")

        elif choice == "2":
            view_questions(data)

        elif choice == "3":
            save_data(data)
            print("Goodbye!")
            break

        elif choice == "4":
            # Warn them before throwing away unsaved work.
            if unsaved:
                confirm = input("You have unsaved changes. Really exit? (y/n): ").strip().lower()
                if confirm != "y":
                    continue
            print("Exiting without saving. Goodbye!")
            break

        else:
            print("Please enter 1, 2, 3, or 4.")


main()
