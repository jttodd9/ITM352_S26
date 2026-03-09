# src/utils.py
# ITM352 - Spring 2026 - Assignment 1
# Justin
#
# Small helper functions used across multiple files.

import os


# Keeps prompting the player until they type something that's in
# the valid_options list. This is how we make sure no invalid
# input ever gets through anywhere in the app.
def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()

        # If what they typed is in the list, we're done.
        if user_input in valid_options:
            return user_input

        # Otherwise tell them what we expected and ask again.
        print("  That's not valid. Please choose from: " + ", ".join(valid_options))


# Clears the terminal screen between questions so things stay clean.
# Uses "cls" on Windows and "clear" on Mac/Linux.
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Prints the title banner when the app first starts up.
def display_banner():
    print("=" * 50)
    print("     INTERACTIVE QUIZ APPLICATION")
    print("     ITM352 - Spring 2026")
    print("=" * 50)
