# src/question.py
# ============================================================
# Question Model - ITM352 Spring 2026 - Assignment 1
#
# Represents a single quiz question.  Supports:
#   - Multiple answer options (requirement 3)
#   - Multiple correct answers (requirement 4)
#   - Optional hint (requirement 6)
#   - Explanation of the correct answer (requirement 7)
# ============================================================


class Question:
    """
    Data model for a single quiz question.

    Attributes:
        question_text (str):     The question being asked.
        options (list[str]):     Answer choices (e.g. ["a) Rome", "b) Paris"]).
        correct_answers (list):  Letters of the correct choice(s) (e.g. ["b"]).
        hint (str):              An optional hint string.
        explanation (str):       Explanation shown after the question is answered.
        is_multi (bool):         True when more than one answer is correct.
    """

    def __init__(self, question_text, options, correct_answers, hint="", explanation=""):
        """
        Initialise a Question instance.

        Args:
            question_text (str):        The question text.
            options (list[str]):        Answer option strings.
            correct_answers (list[str]):Correct answer letter(s).
            hint (str):                 Optional hint (default empty).
            explanation (str):          Post-answer explanation (default empty).
        """
        self.question_text = question_text
        self.options = options
        self.correct_answers = correct_answers
        self.hint = hint
        self.explanation = explanation
        self.is_multi = len(correct_answers) > 1

    def is_correct(self, user_answers):
        """
        Check whether the user's answers exactly match the correct answers.
        Order does not matter.

        Args:
            user_answers (list[str]): Letters chosen by the user.

        Returns:
            bool: True if user_answers match correct_answers (order-insensitive).
        """
        return sorted(user_answers) == sorted(self.correct_answers)

    def get_valid_letters(self):
        """
        Return the set of valid answer letters derived from the options list.

        Returns:
            set[str]: e.g. {'a', 'b', 'c', 'd'}
        """
        return {opt[0].lower() for opt in self.options}

    @classmethod
    def from_dict(cls, data):
        """
        Create a Question from a dictionary (as loaded from questions.json).

        Args:
            data (dict): Must contain 'question', 'options', 'correct'.
                         Optionally 'hint' and 'explanation'.

        Returns:
            Question: A new Question instance.
        """
        return cls(
            question_text=data["question"],
            options=data["options"],
            correct_answers=data["correct"],
            hint=data.get("hint", ""),
            explanation=data.get("explanation", "")
        )
