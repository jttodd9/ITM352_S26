# src/utils.py
# ============================================================
# Utility Module - ITM352 Spring 2026 - Assignment 1
#
# Shared helper functions used throughout the quiz application.
# ============================================================

import os


def get_valid_input(prompt, valid_options):
    """
    Repeatedly prompt the user until they enter one of the accepted values.
    Ensures no invalid response is accepted (a core assignment requirement).

    Args:
        prompt (str):           The text to display before each input attempt.
        valid_options (list):   Acceptable string values (case-insensitive).

    Returns:
        str: A value that is guaranteed to be in valid_options.
    """
    # Normalise valid options to lowercase for comparison
    valid_lower = [v.lower() for v in valid_options]

    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_lower:
            return user_input
        options_str = ", ".join(valid_options)
        print(f"  Invalid input. Please choose from: {options_str}")


def clear_screen():
    """Clear the terminal screen for a cleaner display between questions."""
    os.system("cls" if os.name == "nt" else "clear")


def display_banner():
    """Print the application title banner at startup."""
    print("=" * 50)
    print("     INTERACTIVE QUIZ APPLICATION")
    print("     ITM352 — Spring 2026")
    print("=" * 50)
