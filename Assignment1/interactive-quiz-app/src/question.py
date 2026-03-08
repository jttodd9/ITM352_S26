# src/question.py
# ITM352 - Spring 2026 - Assignment 1
# Justin
#
# Data class for a single quiz question. I made this a class so there's
# one clear place that defines what a question looks like and how to
# check if an answer is correct. That way quiz.py doesn't have to know
# anything about the internal structure of a question dict.


class Question:
    """
    Represents one quiz question with its options, correct answers,
    optional hint, and explanation.

    Supports both single-answer and multi-answer questions -- the only
    difference is how many items are in correct_answers.
    """

    def __init__(self, question_text, options, correct_answers, hint="", explanation=""):
        self.question_text = question_text
        self.options = options          # e.g. ["a) Rome", "b) Paris", ...]
        self.correct_answers = correct_answers  # e.g. ["b"] or ["a","c","d"]
        self.hint = hint
        self.explanation = explanation
        self.is_multi = len(correct_answers) > 1  # handy flag for display logic

    def is_correct(self, user_answers):
        """
        Checks if what the user entered matches the correct answers.
        We sort both lists so the order the user typed them in doesn't matter.
        """
        return sorted(user_answers) == sorted(self.correct_answers)

    def get_valid_letters(self):
        """
        Returns the set of letters that are valid answers for this question,
        pulled from the first character of each option string.
        e.g. ["a) Rome", "b) Paris"] -> {'a', 'b'}
        """
        return {opt[0].lower() for opt in self.options}

    @classmethod
    def from_dict(cls, data):
        """
        Convenience method to build a Question directly from a dict as
        loaded from questions.json, so you don't have to unpack it manually.
        """
        return cls(
            question_text=data["question"],
            options=data["options"],
            correct_answers=data["correct"],
            hint=data.get("hint", ""),
            explanation=data.get("explanation", "")
        )
