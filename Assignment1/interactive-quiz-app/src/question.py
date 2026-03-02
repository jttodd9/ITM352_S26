class Question:
    def __init__(self, question_text, answer_options, correct_answer, explanation):
        self.question_text = question_text
        self.answer_options = answer_options
        self.correct_answer = correct_answer
        self.explanation = explanation

    def is_correct(self, answer):
        return answer == self.correct_answer