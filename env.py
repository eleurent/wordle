# encoding: utf-8
import random
from enum import Enum

NUM_TRIES = 6


class Match(Enum):
    GRAY = u'🟫'
    GREEN = u'🟩'
    YELLOW = u'🟨'


def read_words(path):
    with open(path, "r") as f:
        return f.read().split()


class Env():
    def __init__(self):
        self.allowed = read_words('wordle-allowed-guesses.txt')
        self.answers = read_words('wordle-answers-alphabetical.txt')
        self.allowed += self.answers
        self.reset()

    def reset(self):
        self.steps = 0
        self.answer = random.choice(self.answers)

    def is_valid(self, word):
        return word in self.allowed

    def step(self, word):
        self.steps += 1
        print(f"[Guess {self.steps}] {word.upper()}")
        terminal = False
        if not self.is_valid(word):
            print('INVALID')
            terminal = True
        matches = match(word, self.answer)
        print(''.join([m.value for m in matches]))
        if word == self.answer:
            print('YOU WON')
            terminal = True
        return matches, terminal


def match(word, answer):
    word = word.lower()
    matches = [Match.GRAY] * len(word)
    for i, letter in enumerate(word):
        if letter == answer[i]:
            matches[i] = Match.GREEN
    for i, letter in enumerate(word):
        for j, other in enumerate(answer):
            if letter == other and matches[i] != Match.GREEN:
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


