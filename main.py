import random
from enum import Enum

NUM_TRIES = 6


class Match(Enum):
    GRAY = 0
    GREEN = 1
    YELLOW = 2


def read_words(path):
    with open(path, "r") as f:
        return f.read().split()


def match(word, answer):
    word = word.lower()
    matches = [Match.GRAY] * len(word)
    for i, letter in enumerate(word):
        if letter == answer[i]:
            matches[i] = Match.GREEN
        elif letter in answer:
            matches[i] = Match.YELLOW
    return matches


def ask_allowed_word(allowed):
    print('Choose a word')
    word = input()
    if word.lower() not in allowed:
        print('Invalid!')
        return ask_allowed_word(allowed)
    else:
        return word.lower()


def game(answers, allowed):
    answer = random.choice(answers)
    for tries in range(NUM_TRIES):
        word = ask_allowed_word(allowed)
        matches = match(word, answer)
        print(matches)
        if word == answer:
            print('YOU WON!')
            break
    else:
        print(f'YOU LOST. The answer was {answer}')


def main():
     allowed = read_words('wordle-allowed-guesses.txt')
     answers = read_words('wordle-answers-alphabetical.txt')
     allowed += answers
     game(answers, allowed)


if __name__ == '__main__':
    main()
