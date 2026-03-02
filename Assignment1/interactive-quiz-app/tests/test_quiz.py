import unittest
from src.quiz import Quiz
from src.question import Question

class TestQuiz(unittest.TestCase):

    def setUp(self):
        self.questions = [
            Question("What is the capital of France?", ["Paris", "London", "Berlin"], "Paris"),
            Question("What is 2 + 2?", ["3", "4", "5"], "4"),
        ]
        self.quiz = Quiz(self.questions)

    def test_start_quiz(self):
        self.quiz.start_quiz()
        self.assertTrue(self.quiz.current_question_index >= 0)

    def test_ask_question(self):
        question_text, options = self.quiz.ask_question()
        self.assertIn(question_text, ["What is the capital of France?", "What is 2 + 2?"])
        self.assertEqual(len(options), 3)

    def test_display_score(self):
        self.quiz.score = 5
        score_display = self.quiz.display_score()
        self.assertIn("Your score is:", score_display)

if __name__ == '__main__':
    unittest.main()