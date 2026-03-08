# main.py
# ============================================================
# Interactive Quiz Application — Entry Point
# ITM352 Spring 2026 - Assignment 1
#
# Run with:  python main.py
# ============================================================

from src.quiz import Quiz


def main():
    """Create a Quiz instance and start the game."""
    quiz = Quiz()
    quiz.run()


if __name__ == "__main__":
    main()
