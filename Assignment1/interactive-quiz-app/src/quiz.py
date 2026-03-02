class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.current_question_index = 0

    def start_quiz(self):
        print("Welcome to the Interactive Quiz!")
        while self.current_question_index < len(self.questions):
            self.ask_question()
        self.display_score()

    def ask_question(self):
        question = self.questions[self.current_question_index]
        print(f"Question {self.current_question_index + 1}: {question['text']}")
        for idx, option in enumerate(question['options']):
            print(f"{idx + 1}. {option}")
        answer = input("Your answer (number): ")
        if self.is_valid_answer(answer):
            if self.check_answer(question, answer):
                print("Correct!")
                self.score += 1
            else:
                print(f"Wrong! The correct answer was: {question['correct']}")
            self.current_question_index += 1
        else:
            print("Invalid input. Please enter a number corresponding to your answer.")

    def check_answer(self, question, answer):
        return question['options'][int(answer) - 1] == question['correct']

    def is_valid_answer(self, answer):
        return answer.isdigit() and 1 <= int(answer) <= len(self.questions[self.current_question_index]['options'])

    def display_score(self):
        print(f"Your final score is: {self.score}/{len(self.questions)}")