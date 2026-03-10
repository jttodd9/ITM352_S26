import subprocess
import sys
import os

QUIZ_DIR = os.path.join(os.path.dirname(__file__), "Assignment1", "interactive-quiz-app")
QUIZ_MAIN = os.path.join(QUIZ_DIR, "main.py")

# Correct answers per category (for reference)
# history:   c, b, c, a c d, c, c
# science:   c, b, a c d, b, a b d, a
# music:     b, a b d, c, c, a c, c
# nba:       c, c, a c d, c, a b, b
# geography: c, a b d, c, d, b, a b c

# fmt: (name, category_num, answers_list, expect_score_mention)
# Each answer in answers_list corresponds to one question in the category.
# We mix correct, wrong, and hint/5050 usage across 41 runs.
# Category numbers: 1=history, 2=science, 3=music, 4=nba, 5=geography

test_cases = [
    # --- All correct runs ---
    ("Justin Todd", "1", ["c","b","c","a,c,d","c","c"]),        # 1  history all correct
    ("Justin Todd", "2", ["c","b","a,c,d","b","a,b,d","a"]),    # 2  science all correct
    ("Justin Todd", "3", ["b","a,b,d","c","c","a,c","c"]),      # 3  music all correct
    ("Justin Todd", "4", ["c","c","a,c,d","c","a,b","b"]),      # 4  nba all correct
    ("Justin Todd", "5", ["c","a,b,d","c","d","b","a,b,c"]),    # 5  geography all correct

    # --- All wrong runs ---
    ("Justin Todd", "1", ["a","a","a","b","a","a"]),             # 6  history all wrong
    ("Justin Todd", "2", ["a","a","b","a","c","b"]),             # 7  science all wrong
    ("Justin Todd", "3", ["a","c","a","a","b","a"]),             # 8  music all wrong
    ("Justin Todd", "4", ["a","a","b","a","c","a"]),             # 9  nba all wrong
    ("Justin Todd", "5", ["a","c","a","a","a","d"]),             # 10 geography all wrong

    # --- Mixed correct/wrong ---
    ("Justin Todd", "1", ["c","a","c","b","a","c"]),             # 11 history mixed
    ("Justin Todd", "2", ["a","b","a,c,d","a","a,b,d","b"]),    # 12 science mixed
    ("Justin Todd", "3", ["b","c","a","c","b","a"]),             # 13 music mixed
    ("Justin Todd", "4", ["c","a","a,c,d","a","a,b","a"]),      # 14 nba mixed
    ("Justin Todd", "5", ["a","a,b,d","a","d","a","a,b,c"]),    # 15 geography mixed

    # --- Guest (empty name) ---
    ("", "1", ["c","b","c","a,c,d","c","c"]),                   # 16 guest all correct history
    ("", "3", ["a","c","a","a","b","a"]),                        # 17 guest all wrong music
    ("", "5", ["c","a,b,d","c","d","b","a,b,c"]),               # 18 guest all correct geography

    # --- Hint then answer ---
    ("Justin Todd", "1", ["hint","c","b","c","a,c,d","c","c"]),              # 19 hint on Q1 then correct
    ("Justin Todd", "2", ["hint","c","hint","b","a,c,d","b","a,b,d","a"]),   # 20 hints on Q1 and Q3

    # --- 5050 then answer ---
    ("Justin Todd", "1", ["5050","c","b","c","a,c,d","c","c"]),              # 21 5050 on Q1 then correct
    ("Justin Todd", "3", ["5050","b","a,b,d","c","c","a,c","c"]),            # 22 5050 on Q1 then all correct
    ("Justin Todd", "4", ["5050","c","c","a,c,d","c","a,b","b"]),            # 23 5050 on Q1 then all correct

    # --- Invalid input then valid ---
    ("Justin Todd", "2", ["z","c","b","a,c,d","b","a,b,d","a"]),             # 24 invalid then correct on Q1
    ("Justin Todd", "5", ["9","c","a,b,d","c","d","b","a,b,c"]),             # 25 invalid category retries then correct

    # --- Repeat runs as same user (tests high score tracking) ---
    ("Justin Todd", "1", ["c","b","c","a,c,d","c","c"]),        # 26 history all correct again
    ("Justin Todd", "2", ["c","b","a,c,d","b","a,b,d","a"]),    # 27 science all correct again
    ("Justin Todd", "4", ["c","c","a,c,d","c","a,b","b"]),      # 28 nba all correct again

    # --- Half correct ---
    ("Justin Todd", "1", ["c","a","a","a,c,d","a","a"]),         # 29 only Q1 + Q4 correct
    ("Justin Todd", "3", ["a","a,b,d","a","a","a,c","a"]),       # 30 only Q2 + Q5 correct
    ("Justin Todd", "5", ["a","a","c","d","a","a"]),             # 31 only Q3 + Q4 correct

    # --- Different users ---
    ("Alice",       "1", ["c","b","c","a,c,d","c","c"]),         # 32 Alice all correct history
    ("Bob",         "2", ["a","a","b","a","c","b"]),             # 33 Bob all wrong science
    ("Charlie",     "4", ["c","c","a,c,d","c","a,b","b"]),       # 34 Charlie all correct nba
    ("Diana",       "3", ["b","a,b,d","c","c","a,c","c"]),       # 35 Diana all correct music
    ("Eve",         "5", ["c","a,b,d","c","d","b","a,b,c"]),     # 36 Eve all correct geography

    # --- 5050 + wrong answers ---
    # Science Q1 correct=c; 5050 eliminates a,b so remaining are c,d → use d (wrong)
    ("Justin Todd", "2", ["5050","d","a","b","a","c","b"]),      # 37 5050 then wrong answers
    # Music Q1 correct=b; 5050 eliminates a,c so remaining are b,d → use d (wrong)
    ("Justin Todd", "3", ["5050","d","c","a","a","b","a"]),      # 38 5050 then wrong answers music

    # --- Hint + wrong answers ---
    ("Justin Todd", "4", ["hint","a","a","b","a","c","a"]),      # 39 hint then all wrong nba
    ("Justin Todd", "5", ["hint","a","c","a","a","a","d"]),      # 40 hint then all wrong geo

    # --- Perfect score science ---
    ("Justin Todd", "2", ["c","b","a,c,d","b","a,b,d","a"]),    # 41 science perfect again
]

passed = 0
failed = 0
errors = []

for i, (name, cat, answers) in enumerate(test_cases, 1):
    # Build stdin: name, category, press Enter to start, then answers
    lines = [name, cat, ""] + answers
    user_input = "\n".join(lines) + "\n"

    result = subprocess.run(
        [sys.executable, "main.py"],
        input=user_input,
        capture_output=True,
        text=True,
        cwd=QUIZ_DIR
    )

    out = result.stdout

    # Basic checks: program ran and printed the quiz complete banner
    if result.returncode == 0 and "QUIZ COMPLETE" in out:
        # Determine expected player name display
        display_name = name if name != "" else "guest"
        if display_name in out:
            print(f"Test {i:2d}: PASS | User: {display_name!r:14s} | Cat: {cat} | Answers: {answers}")
            passed += 1
        else:
            print(f"Test {i:2d}: FAIL | Name '{display_name}' not found in output")
            errors.append(i)
            failed += 1
    else:
        stderr_snippet = result.stderr.strip()[:120] if result.stderr else ""
        stdout_snippet = out.strip()[-200:] if out else ""
        print(f"Test {i:2d}: FAIL | returncode={result.returncode}")
        if stderr_snippet:
            print(f"         stderr: {stderr_snippet}")
        if stdout_snippet:
            print(f"         stdout tail: {stdout_snippet}")
        errors.append(i)
        failed += 1

print(f"\n{'='*60}")
print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
if errors:
    print(f"Failed tests: {errors}")
