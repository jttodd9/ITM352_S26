# main.py
# ITM352 - Spring 2026 - Assignment 1
# Justin
#
# Entry point for the quiz app. All it does is kick off the Quiz class --
# the actual game logic lives in src/quiz.py.
#
# Run the quiz:        python main.py
# Add new questions:   python question_creator.py

from src.quiz import Quiz


def main():
    # Create a quiz and start it -- Quiz loads the questions automatically
    quiz = Quiz()
    quiz.run()


if __name__ == "__main__":
    main()
