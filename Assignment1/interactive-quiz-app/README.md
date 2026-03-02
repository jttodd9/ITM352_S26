# Interactive Quiz Application

This project is an interactive quiz application that allows users to test their knowledge on various topics through a series of questions. The application is designed to be user-friendly and engaging, providing instant feedback on answers and tracking scores.

## Features

- **Interactive Quiz Flow**: Users can start the quiz, answer questions, and receive immediate feedback.
- **Question Management**: Questions are stored in a JSON file, making it easy to update and manage the quiz content.
- **Score Tracking**: The application tracks user scores and can determine if a new high score has been achieved.
- **Utility Functions**: Includes input validation and hint generation to enhance user experience.

## Project Structure

```
interactive-quiz-app
├── src
│   ├── __init__.py
│   ├── quiz.py
│   ├── question.py
│   ├── scoring.py
│   └── utils.py
├── data
│   └── questions.json
├── tests
│   ├── __init__.py
│   ├── test_quiz.py
│   ├── test_question.py
│   └── test_scoring.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd interactive-quiz-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To start the quiz application, run the following command:
```
python main.py
```

Follow the on-screen instructions to answer the questions and see your score at the end of the quiz.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.