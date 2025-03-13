def preprocessing(puzzle_input: str):
    lines = puzzle_input.splitlines()
    guesses = [guess.split() for guess in lines[:3]]
    absent = set()
    correct_pos = {}
    wrong_pos = {}
    for attempt, result in guesses:
        for i, (l, r) in enumerate(zip(attempt, result)):
            if r == 'B':
                absent.add(l)
            elif r == 'G':
                correct_pos[i] = l
            else:
                wrong_pos[l] = i
    words = lines[3:]
    return words, absent, correct_pos, wrong_pos

def solver(words, absent, correct_pos, wrong_pos):
    for word in words:
        if any(c in absent for c in word):
            continue
        if any(word[i] != l for i, l in correct_pos.items()):
            continue
        if any(l not in word or word[i] == l for l, i in wrong_pos.items()):
            continue

        return word
    