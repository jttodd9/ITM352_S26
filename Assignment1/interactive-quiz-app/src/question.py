# src/question.py
# ITM352 - Spring 2026 - Assignment 1
# Justin
#
# Helper functions for working with a question dictionary.
# A question in the JSON looks like this:
#
#   {
#       "question":    "What is 2 + 2?",
#       "options":     ["a) 3", "b) 4", "c) 5", "d) 6"],
#       "correct":     ["b"],
#       "hint":        "Think single digits.",
#       "explanation": "2 + 2 equals 4."
#   }


# Checks if the player's answers match the correct ones.
# Sorts both lists first so the order they typed them in doesn't matter.
def is_correct(question, user_answers):
    return sorted(user_answers) == sorted(question["correct"])


# Builds and returns the list of valid answer letters for a question.
# Grabs the first character from each option string, e.g. "a) Rome" -> "a".
def get_valid_letters(question):
    letters = []
    for opt in question["options"]:
        letters.append(opt[0].lower())
    return letters
