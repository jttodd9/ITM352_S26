# src/utils.py
# ITM352 - Spring 2026 - Assignment 1
# Justin
#
# Small helper functions that get used in multiple places.
# I put them here so I'm not copy-pasting the same input loop everywhere.

import os


def get_valid_input(prompt, valid_options):
    """
    Keeps asking the user for input until they enter something valid.
    This is how we make sure no invalid response ever gets through --
    the loop just keeps re-prompting until they give us something in the list.

    Comparison is case-insensitive so "A" and "a" both work.
    """
    valid_lower = [v.lower() for v in valid_options]

    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_lower:
            return user_input
        # Show them what we actually want
        print(f"  That's not valid. Please choose from: {', '.join(valid_options)}")


def clear_screen():
    """Clears the terminal between questions so the screen doesn't get cluttered."""
    os.system("cls" if os.name == "nt" else "clear")


def display_banner():
    """Prints the title screen when the app starts."""
    print("=" * 50)
    print("     INTERACTIVE QUIZ APPLICATION")
    print("     ITM352 — Spring 2026")
    print("=" * 50)
