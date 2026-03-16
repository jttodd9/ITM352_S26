# Read the JSON file created in Ex5 and print it

import json

with open("quiz_questions.json", "r") as f:
    quiz_data = json.load(f)

print(json.dumps(quiz_data, indent=4))
