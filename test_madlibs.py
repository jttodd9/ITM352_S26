import subprocess
import sys

# 38 different sets of Mad Libs answers
test_cases = [
    ["Justin Todd", "silly", "banana", "running", "enormous", "castle", "jump", "dragon", "pizza", "5"],
    ["Justin Todd", "happy", "rocket", "dancing", "tiny", "mountain", "laugh", "unicorn", "tacos", "3"],
    ["Justin Todd", "grumpy", "spaghetti", "flying", "magical", "volcano", "scream", "penguin", "sushi", "10"],
    ["Justin Todd", "brave", "toaster", "swimming", "fuzzy", "spaceship", "sing", "hamster", "burger", "7"],
    ["Justin Todd", "loud", "umbrella", "bouncing", "spooky", "treasure", "run", "elephant", "ice cream", "2"],
    ["Justin Todd", "purple", "calculator", "spinning", "wobbly", "library", "clap", "robot", "noodles", "99"],
    ["Justin Todd", "shiny", "pickle", "laughing", "ancient", "skyscraper", "sneeze", "flamingo", "waffles", "4"],
    ["Justin Todd", "clumsy", "watermelon", "skipping", "invisible", "submarine", "yell", "raccoon", "cookies", "12"],
    ["Justin Todd", "magical", "telephone", "crawling", "glittery", "jungle", "hiss", "narwhal", "spaghetti", "6"],
    ["Justin Todd", "fantastic", "shoe", "zooming", "rusty", "laboratory", "meow", "capybara", "donuts", "8"],
    ["Justin Todd", "wobbly", "cloud", "stomping", "mysterious", "fortress", "bark", "octopus", "pie", "15"],
    ["Justin Todd", "electric", "noodle", "hopping", "gigantic", "cave", "growl", "parrot", "salad", "1"],
    ["Justin Todd", "frozen", "sandwich", "sliding", "fluffy", "tower", "whistle", "koala", "ramen", "20"],
    ["Justin Todd", "spicy", "lamp", "galloping", "slimy", "dungeon", "roar", "platypus", "cake", "9"],
    ["Justin Todd", "bouncy", "window", "wiggling", "sparkling", "island", "chirp", "pangolin", "chips", "13"],
    ["Justin Todd", "ancient", "trumpet", "tiptoeing", "crispy", "swamp", "moo", "axolotl", "pancakes", "17"],
    ["Justin Todd", "neon", "pillow", "marching", "wobbly", "forest", "squeak", "sloth", "pasta", "11"],
    ["Justin Todd", "gigantic", "doorknob", "twirling", "sparkly", "glacier", "honk", "mongoose", "burritos", "25"],
    ["Justin Todd", "invisible", "stapler", "prancing", "electric", "pyramid", "woof", "alpaca", "popcorn", "30"],
    ["Justin Todd", "sticky", "spatula", "waddling", "crunchy", "waterfall", "hoot", "dolphin", "sushi", "14"],
    ["Justin Todd", "fluffy", "guitar", "leaping", "mega", "volcano", "neigh", "llama", "tacos", "16"],
    ["Justin Todd", "rusty", "cactus", "zooming", "bubbly", "crater", "ribbit", "fox", "mochi", "18"],
    ["Justin Todd", "crispy", "mailbox", "shuffling", "sticky", "meadow", "tweet", "hedgehog", "gyros", "22"],
    ["Justin Todd", "wiggly", "backpack", "zipping", "neon", "canyon", "purr", "wombat", "curry", "19"],
    ["Justin Todd", "shimmery", "notebook", "rocketing", "super", "reef", "baa", "ferret", "gelato", "21"],
    ["Justin Todd", "ferocious", "teapot", "lumbering", "glowing", "tundra", "cluck", "meerkat", "falafel", "23"],
    ["Justin Todd", "dreamy", "escalator", "bounding", "enormous", "oasis", "oink", "quokka", "churros", "24"],
    ["Justin Todd", "bubbly", "frying pan", "sauntering", "ancient", "cliff", "quack", "armadillo", "pho", "26"],
    ["Justin Todd", "sparkly", "telescope", "scrambling", "neon", "lagoon", "gobble", "toucan", "shawarma", "27"],
    ["Justin Todd", "twisty", "refrigerator", "shuffling", "mega", "marsh", "bray", "bison", "tiramisu", "28"],
    ["Justin Todd", "glowing", "saxophone", "somersaulting", "ancient", "mesa", "warble", "iguana", "empanadas", "29"],
    ["Justin Todd", "crunchy", "hammock", "skidding", "bubbly", "ravine", "trill", "chinchilla", "baklava", "31"],
    ["Justin Todd", "dazzling", "microscope", "cartwheeling", "ferocious", "dune", "caw", "tapir", "samosa", "32"],
    ["Justin Todd", "glittery", "accordion", "pirouetting", "twisty", "inlet", "grunt", "emu", "pierogi", "33"],
    ["Justin Todd", "electrifying", "doorbell", "catapulting", "dazzling", "atoll", "bellow", "kinkajou", "bibimbap", "34"],
    ["Justin Todd", "magnificent", "blender", "orbiting", "magnificent", "fjord", "yap", "numbat", "poutine", "35"],
    ["Justin Todd", "colossal", "staple gun", "teleporting", "colossal", "butte", "bay", "fossa", "knish", "36"],
    ["Justin Todd", "legendary", "kazoo", "moonwalking", "legendary", "atoll", "toot", "quoll", "baozi", "37"],
]

passed = 0
failed = 0

for i, answers in enumerate(test_cases, 1):
    user_input = "\n".join(answers) + "\n"
    result = subprocess.run(
        [sys.executable, "Lab1/Ex1.py"],
        input=user_input,
        capture_output=True,
        text=True
    )

    if result.returncode == 0 and answers[0] in result.stdout:
        print(f"Test {i:2d}: PASS | Name: {answers[0]}, Animal: {answers[7]}, Food: {answers[8]}")
        passed += 1
    else:
        print(f"Test {i:2d}: FAIL | stderr: {result.stderr.strip()}")
        failed += 1

print(f"\n{'='*50}")
print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
