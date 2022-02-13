# encoding: utf-8
import random
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Match(Enum):
    GRAY = u'🟫'
    GREEN = u'🟩'
    YELLOW = u'🟨'


class Env:
    NUM_TRIES: int = 6

    def __init__(self):
        self.allowed = self.read_words('wordle-allowed-guesses.txt')
        self.answers = self.read_words('wordle-answers-alphabetical.txt')
        self.allowed += self.answers
        self.steps = 0
        self.answer = None
        self.reset()

    def step(self, word):
        self.steps += 1
        logger.info(f"[Guess {self.steps}] {word.upper()}")
        terminal = False
        if not self.is_valid(word):
            logger.error('Invalid word')
            terminal = True
        matches = self.match(word, self.answer)
        logger.info(''.join([m.value for m in matches]))
        if word == self.answer:
            logger.info('YOU WON!')
            terminal = True
        elif self.steps == self.NUM_TRIES:
            logger.info(f'YOU LOST. The answer was {self.answer}')
            terminal = True
        return matches, terminal

    def reset(self):
        self.steps = 0
        self.answer = random.choice(self.answers)

    def is_valid(self, word):
        return word in self.allowed

    @staticmethod
    def read_words(path):
        with open(path, "r") as f:
            return f.read().split()

    @staticmethod
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
