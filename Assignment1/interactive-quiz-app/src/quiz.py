# src/quiz.py
# ITM352 - Spring 2026 - Assignment 1
# Justin
#
# All the quiz logic lives here as plain functions.
# run_quiz() is the main one, it calls all the others in order.

import json
import os
import time

from src.scoring import load_scores, save_score, get_grand_champion
from src.utils import get_valid_input, clear_screen, display_banner

# Path to the questions file, built so it works from any directory.
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "questions.json")

# How fast the player needs to answer to earn a bonus point.
BONUS_THRESHOLD = 10
BONUS_POINTS = 1


# Opens questions.json and returns the categories dictionary.
# Returns an empty dict instead of crashing if the file is missing
# or has a formatting error.
def load_questions():
    try:
        file = open(QUESTIONS_FILE, "r")
        data = json.load(file)
        file.close()
        return data["categories"]
    except FileNotFoundError:
        print("Error: could not find the questions file.")
        return {}
    except json.JSONDecodeError:
        print("Error: questions file has a formatting problem.")
        return {}


# Asks the player for a name and loads their saved stats.
# Shows their personal best and the grand champion if either exists.
# Returns the name string so run_quiz() can use it later.
def get_username():
    print("\n" + "=" * 50)
    print("Enter your name, or press Enter to play as guest:")
    name = input("> ").strip()

    # Default to guest if they just hit Enter.
    if name == "":
        name = "guest"

    print("\nWelcome, " + name + "!")

    # Load scores so we can show their history right at login.
    scores = load_scores()

    # Only show a personal best if they've played before.
    if name in scores["users"]:
        best = scores["users"][name]["high_score"]
        print("  Your personal best: " + str(best) + " points")

    # Show the grand champion so there's something to aim for.
    champion = get_grand_champion(scores)
    if champion is not None:
        print("  Grand Champion: " + champion["name"] + " - " + str(champion["score"]) + " points")

    return name


# Shows all the categories from the JSON and lets the player pick one.
# Keeps re-prompting if they type something that isn't a valid number.
# Returns the chosen category name as a string.
def choose_category(categories):
    # Pull the category names into a list so we can index them by number.
    category_list = list(categories.keys())

    print("\n" + "=" * 50)
    print("Pick a category:")

    # Print each category with its number and question count.
    i = 1
    for cat in category_list:
        count = len(categories[cat])
        print("  " + str(i) + ". " + cat.title() + "  (" + str(count) + " questions)")
        i = i + 1

    # Build the list of numbers we'll accept as input.
    valid = []
    for i in range(1, len(category_list) + 1):
        valid.append(str(i))

    choice = get_valid_input("Enter a number: ", valid)

    # Subtract 1 because lists are zero-indexed but our menu starts at 1.
    chosen = category_list[int(choice) - 1]
    return chosen


# Converts whatever the player typed into a clean list of letters.
# Handles formats like "b", "a,c", "a, c", and "acd".
# Returns an empty list if the input contains anything that isn't a letter.
def parse_answer(user_input):
    # Strip commas and spaces first so all the formats end up the same.
    cleaned = user_input.replace(",", "").replace(" ", "")

    # Split the string into one character per item in the list.
    letters = []
    for char in cleaned:
        letters.append(char)

    # Reject the whole input if any character isn't a letter.
    for char in letters:
        if not char.isalpha():
            return []

    return letters


# Finds all the wrong-answer letters and returns the first two.
# Used by the 50/50 lifeline to decide which options to hide.
def apply_fifty_fifty(options, correct_answers):
    # Collect every option letter that isn't in the correct answers list.
    wrong = []
    for opt in options:
        letter = opt[0].lower()
        if letter not in correct_answers:
            wrong.append(letter)

    # Only grab two at most, even if there are more wrong answers.
    eliminated = []
    if len(wrong) >= 1:
        eliminated.append(wrong[0])
    if len(wrong) >= 2:
        eliminated.append(wrong[1])

    return eliminated


# Shows one question and loops until the player gives a valid answer.
# Handles hints, 50/50, multi-letter input, timing, correctness,
# and the explanation all in one place.
# Returns a tuple: (is_correct, fifty_fifty_used, elapsed_seconds).
def ask_question(question_data, question_num, fifty_fifty_used):
    correct_answers = question_data["correct"]

    # Check upfront if this question needs more than one answer.
    is_multi = len(correct_answers) > 1

    print("\n" + question_data["question"])
    if is_multi:
        # Let the player know before they see the options.
        print("(Multiple correct answers -- enter all of them, e.g. 'a,c')")

    options = list(question_data["options"])

    # eliminated tracks which letters the 50/50 removed.
    eliminated = []

    # Start the clock the moment the question appears on screen.
    start_time = time.time()

    while True:

        # Only print options that haven't been eliminated yet.
        print()
        for opt in options:
            letter = opt[0].lower()
            if letter not in eliminated:
                print("  " + opt)

        # Only show a command if it's actually usable at this point.
        if question_data.get("hint") and len(eliminated) == 0:
            print("  [type 'hint' for a hint]")
        if not fifty_fifty_used and len(eliminated) == 0:
            print("  [type '5050' to remove two wrong answers]")

        user_input = input("\nYour answer: ").strip().lower()

        # Show the hint and loop back without counting it as an answer.
        if user_input == "hint":
            hint_text = question_data.get("hint", "")
            if hint_text != "":
                print("\nHint: " + hint_text)
            else:
                print("\nNo hint available for this one.")
            continue

        # Apply 50/50 and loop back, the player still needs to answer.
        if user_input == "5050":
            if fifty_fifty_used:
                print("\nYou already used 50/50 this game!")
                continue
            eliminated = apply_fifty_fifty(options, correct_answers)
            fifty_fifty_used = True
            print("\n50/50 used -- two wrong answers are gone.")
            continue

        # Turn the raw input into a list of letters.
        parsed = parse_answer(user_input)

        # Build the list of letters still on the board after any 50/50.
        available = []
        for opt in options:
            letter = opt[0].lower()
            if letter not in eliminated:
                available.append(letter)

        # Reject if the input was empty or had a letter not on the board.
        valid_input = True
        if len(parsed) == 0:
            valid_input = False
        else:
            for letter in parsed:
                if letter not in available:
                    valid_input = False

        if not valid_input:
            print("\nInvalid input. Please enter from: " + ", ".join(available))
            continue

        # Reject duplicate letters like "a,a".
        seen = []
        has_duplicate = False
        for letter in parsed:
            if letter in seen:
                has_duplicate = True
            seen.append(letter)

        if has_duplicate:
            print("\nYou entered the same letter more than once.")
            continue

        # Stop the clock now that we have a real answer.
        elapsed = time.time() - start_time

        # Sort both lists so the order the player typed doesn't matter.
        is_correct = sorted(parsed) == sorted(correct_answers)

        if is_correct:
            print("\nCorrect!")
        else:
            # Show what the right answers were so they know what they missed.
            correct_display = ", ".join(correct_answers).upper()
            print("\nIncorrect. The correct answer(s): " + correct_display)

        print("Time: " + str(round(elapsed, 1)) + "s")

        # Always show the explanation so the player learns something.
        explanation = question_data.get("explanation", "")
        if explanation != "":
            print("\nExplanation: " + explanation)

        # Hand the results back to run_quiz() and move on.
        return is_correct, fifty_fifty_used, elapsed


# The main function that ties everything together.
# Runs the full quiz from the banner screen to the final score printout.
def run_quiz():
    display_banner()

    # Get a name and show any existing stats for that player.
    username = get_username()

    # Load the questions file and bail out if it failed.
    categories = load_questions()
    if len(categories) == 0:
        return

    # Let the player pick which category they want to be quizzed on.
    category = choose_category(categories)
    questions = categories[category]

    print("\nAlright, " + category.title() + " it is!")
    print(str(len(questions)) + " questions coming up.\n")
    print("How it works:")
    print("  Type a letter to answer                 (e.g. 'b')")
    print("  For multi-answer questions use commas   (e.g. 'a,c')")
    print("  Type 'hint' for a hint")
    print("  Type '5050' to eliminate 2 wrong answers (once per game)")
    print("  Answer in under " + str(BONUS_THRESHOLD) + " seconds for a +" + str(BONUS_POINTS) + " speed bonus!")
    input("\nPress Enter when you're ready...")

    # These three variables track everything that changes during the quiz.
    score = 0
    bonus_score = 0
    fifty_fifty_used = False

    # Go through every question in order.
    for i in range(len(questions)):
        clear_screen()

        # Show the running total so the player can see how they're doing.
        running_total = score + bonus_score
        print("\n--- Question " + str(i + 1) + " of " + str(len(questions)) +
              " | Score: " + str(running_total) + " ---")

        # ask_question handles all the interaction and returns the results.
        is_correct, fifty_fifty_used, elapsed = ask_question(questions[i], i + 1, fifty_fifty_used)

        if is_correct:
            score = score + 1
            # Award the speed bonus if they were fast enough.
            if elapsed <= BONUS_THRESHOLD:
                bonus_score = bonus_score + BONUS_POINTS
                print("Speed bonus! +" + str(BONUS_POINTS) + " point for answering in " + str(round(elapsed, 1)) + "s")

        print()

    # Add base score and bonus together for the final number.
    total = score + bonus_score

    # Avoid dividing by zero if somehow there are no questions.
    if len(questions) > 0:
        percentage = (score / len(questions)) * 100
    else:
        percentage = 0

    clear_screen()
    print("\n" + "=" * 50)
    print("  QUIZ COMPLETE!")
    print("=" * 50)
    print("  Player:       " + username)
    print("  Category:     " + category.title())
    print("  Base Score:   " + str(score) + " / " + str(len(questions)) + "  (" + str(round(percentage)) + "%)")
    print("  Bonus Points: " + str(bonus_score))
    print("  TOTAL:        " + str(total))
    print("=" * 50)

    # Give the player a message based on how well they did.
    if percentage == 100:
        print("  Perfect score!")
    elif percentage >= 70:
        print("  Great job!")
    elif percentage >= 50:
        print("  Not bad, keep studying!")
    else:
        print("  Better luck next time!")

    # Save to file and find out if they beat their own record.
    scores = load_scores()
    is_new_high = save_score(scores, username, category, total)

    if is_new_high:
        print("\n*** New personal high score for " + username + "! ***")

    # Reload the scores after saving so we get the updated champion.
    champion = get_grand_champion(load_scores())
    if champion is not None:
        print("\nGrand Champion: " + champion["name"] + " - " + str(champion["score"]) + " points")

    print("\nThanks for playing!\n")
