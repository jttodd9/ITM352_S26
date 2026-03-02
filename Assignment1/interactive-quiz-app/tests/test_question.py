import unittest
from src.question import Question

class TestQuestion(unittest.TestCase):

    def setUp(self):
        self.question = Question(
            text="What is the capital of France?",
            options=["Berlin", "Madrid", "Paris", "Rome"],
            correct_answer="Paris",
            explanation="Paris is the capital city of France."
        )

    def test_is_correct_with_correct_answer(self):
        self.assertTrue(self.question.is_correct("Paris"))

    def test_is_correct_with_incorrect_answer(self):
        self.assertFalse(self.question.is_correct("Berlin"))

    def test_question_text(self):
        self.assertEqual(self.question.text, "What is the capital of France?")

    def test_options(self):
        self.assertEqual(self.question.options, ["Berlin", "Madrid", "Paris", "Rome"])

    def test_explanation(self):
        self.assertEqual(self.question.explanation, "Paris is the capital city of France.")

if __name__ == '__main__':
    unittest.main()