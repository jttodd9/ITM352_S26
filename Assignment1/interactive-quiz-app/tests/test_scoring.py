import unittest
from src.scoring import save_score, check_high_score

class TestScoring(unittest.TestCase):

    def setUp(self):
        self.test_score_file = 'test_scores.txt'
        self.high_score = 100

    def test_save_score(self):
        save_score(self.test_score_file, self.high_score)
        with open(self.test_score_file, 'r') as file:
            saved_score = int(file.read().strip())
        self.assertEqual(saved_score, self.high_score)

    def test_check_high_score(self):
        self.assertTrue(check_high_score(self.high_score, self.test_score_file))
        self.assertFalse(check_high_score(50, self.test_score_file))

    def tearDown(self):
        import os
        if os.path.exists(self.test_score_file):
            os.remove(self.test_score_file)

if __name__ == '__main__':
    unittest.main()