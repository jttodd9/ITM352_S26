def save_score(score, filename='scores.txt'):
    with open(filename, 'a') as file:
        file.write(f"{score}\n")

def check_high_score(score, filename='scores.txt'):
    try:
        with open(filename, 'r') as file:
            high_scores = [int(line.strip()) for line in file.readlines()]
            return score > max(high_scores) if high_scores else True
    except FileNotFoundError:
        return True