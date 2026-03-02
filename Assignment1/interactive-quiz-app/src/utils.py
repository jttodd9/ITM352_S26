def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip()
        if user_input in valid_options:
            return user_input
        print(f"Invalid input. Please choose from: {', '.join(valid_options)}")

def provide_hint(question):
    if hasattr(question, 'hint'):
        return question.hint
    return "No hint available for this question."