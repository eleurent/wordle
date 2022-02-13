from collections import Counter
from operator import itemgetter
import random
import logging

from env import Env, Match

logger = logging.getLogger(__name__)


class AbstractAgent:
    def act(self):
        raise NotImplementedError

    def observe(self, word, matches):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError


class InputAgent(AbstractAgent):
    def __init__(self, env: Env):
        self.env = env

    def act(self):
        logger.info('Choose a word')
        word = input()
        if word.lower() not in self.env.allowed:
            logger.info('Invalid word, try again.')
            return self.act()
        else:
            return word.lower()

    def observe(self, word, matches):
        pass

    def reset(self):
        pass


class ArianeAgent(AbstractAgent):
    def __init__(self, env: Env):
        self.env = env
        self.alphabet = set('qwertyuiopasdfghjklzxcvbnm')
        self.greens = self.grays = self.yellows = {}
        self.openings = []
        self.candidate_words = []
        self.reset()

    def reset(self):
        self.greens = {}
        self.grays = set()
        self.yellows = {}
        self.openings = self.find_good_openings()
        self.candidate_words = self.env.answers.copy()

    def act(self):
        if self.openings:
            return self.openings.pop()
        else:
            return random.choice(self.candidate_words)

    def observe(self, word, matches):
        if self.openings and len(self.found_letters) >= 4:
            self.openings = []
        self.update_letters_lists(matches, word)
        self.update_candidate_words()
        logger.info(f'{len(self.candidate_words)} words and {len(self.candidate_letters)} letters remaining.')
        if len(self.candidate_words) < 5:
            logger.info(self.candidate_words)
        logger.info(f'Greens: {self.greens}')
        logger.info(f'Yellows: {self.yellows}')
        logger.info(f'Grays: {self.grays}')

    def update_letters_lists(self, matches, word):
        for i, (match, letter) in enumerate(zip(matches, word)):
            if match == Match.GRAY:
                self.grays.add(letter)
            elif match == Match.GREEN:
                if letter in self.yellows:
                    self.yellows.pop(letter)
                self.greens[letter] = i
            elif match == Match.YELLOW:
                if letter in self.yellows:
                    if i in self.yellows[letter]:
                        self.yellows[letter].remove(i)
                else:
                    self.yellows[letter] = [j for j in range(5) if (j != i and j not in self.greens)]

    def update_candidate_words(self):
        valid_words = []
        for word in self.candidate_words:
            valid = True
            for letter in self.grays:
                if letter in word:
                    valid = False
            for letter, i in self.greens.items():
                if word[i] != letter:
                    valid = False
            for letter, positions in self.yellows.items():
                if not any(word[i] == letter for i in positions):
                    valid = False
            if valid:
                valid_words.append(word)
        self.candidate_words = valid_words

    @property
    def found_letters(self):
        return set(self.greens.keys()).union(self.yellows.keys())

    @property
    def candidate_letters(self):
        return self.alphabet.difference(self.grays)

    def find_good_openings(self):
        frequent_letters = self.most_frequent_letters(self.env.answers)
        logger.info(f"Most frequent letters: {frequent_letters}")
        frequent_letters = [letter for letter, count in frequent_letters]
        return self.good_openings(self.env.allowed, frequent_letters)

    @staticmethod
    def letter_counts(answers):
        return Counter([l for w in answers for l in w])

    @staticmethod
    def most_frequent_letters(answers, count=15):
        return sorted(ArianeAgent.letter_counts(answers).items(), key=itemgetter(1), reverse=True)[:count]

    @staticmethod
    def good_openings(words, frequent_letters):
        openings = ['runty', 'pechs', 'dolia']  # Hardcoded values, obtained from running the following once
        if openings:
            random.shuffle(openings)
            return openings
        letters = frequent_letters
        word1 = word2 = word3 = None
        while not word1:
            word1, w1_letters = ArianeAgent.find_word_with_letter_list(words, letters)
            logger.info(f'Found word1 {word1}, remaining {w1_letters}')
            word2 = None
            while not word2:
                word2, w2_letters = ArianeAgent.find_word_with_letter_list(words, w1_letters)
                logger.info(f'Found word2 {word2}, remaining {w2_letters}')
                for _ in range(10):
                    word3, _ = ArianeAgent.find_word_with_letter_list(words, w2_letters)
                    if word3:
                        break
                else:
                    word2 = None
        return [word1, word2, word3]

    @staticmethod
    def find_word_with_letter_list(words, letters):
        word = remaining = None
        while not word:
            chosen, remaining = ArianeAgent.choose_letters_in_list(letters)
            logger.info(f'Chose letters {chosen}, remaining {remaining}')
            word = ArianeAgent.find_word_with_letters(words, chosen)
        return word, remaining

    @staticmethod
    def choose_letters_in_list(letters, count=5):
        chosen = random.sample(letters, count)
        return chosen, [letter for letter in letters if letter not in chosen]

    @staticmethod
    def find_word_with_letters(words, letters):
        for word in words:
            if set(word) == set(letters):
                return word
        else:
            return None

