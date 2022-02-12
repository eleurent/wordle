from collections import Counter
from operator import itemgetter
import random

from env import Env, Match


class Agent():
    def __init__(self, env):
        self.env = env
        self.alphabet = set('qwertyuiopasdfghjklzxcvbnm')
        self.greens = {}
        self.grays = set()
        self.yellows = {}
        self.openings = self.find_good_openings()
        self.candidate_words = env.answers.copy()

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
            for l in self.grays:
                if l in word:
                    valid = False
            for l, i in self.greens.items():
                if word[i] != l:
                    valid = False
            for l, positions in self.yellows.items():
                if not any(word[i] == l for i in positions):
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

    def play_word(self, word):
        matches, terminal = self.env.step(word)
        if terminal:
            return terminal
        self.update_letters_lists(matches, word)
        self.update_candidate_words()
        print(f'{len(self.candidate_words)} words and {len(self.candidate_letters)} letters remaining.')
        if len(self.candidate_words) < 5:
            print(self.candidate_words)
        print(f'Greens: {self.greens}')
        print(f'Yellows: {self.yellows}')
        print(f'Grays: {self.grays}')
        return terminal

    def find_good_openings(self):
        frequent_letters = most_frequent_letters(self.env.answers)
        print("Most frequent letters", frequent_letters)
        frequent_letters = [l for l, c in frequent_letters]
        return good_openings(self.env.allowed, frequent_letters)

    def act(self):
        if self.openings:
            word = self.openings.pop()
            terminal = self.play_word(word)
            if len(self.found_letters) >= 4:
                self.openings = []
        else:
            terminal = self.play_word(random.choice(self.candidate_words))
        return terminal


def letter_counts(answers):
    return Counter([l for w in answers for l in w])


def most_frequent_letters(answers, count=15):
    return sorted(letter_counts(answers).items(), key=itemgetter(1), reverse=True)[:count]


def good_openings(words, frequent_letters):
    openings = ['runty', 'pechs', 'dolia']
    random.shuffle(openings)
    return openings
    letters = frequent_letters
    word1 = None
    while not word1:
        word1, w1_letters = find_word_with_letter_list(words, letters)
        print(f'Found word1 {word1}, remaining {w1_letters}')
        word2 = None
        while not word2:
            word2, w2_letters = find_word_with_letter_list(words, w1_letters)
            print(f'Found word2 {word2}, remaining {w2_letters}')
            for _ in range(10):
                word3, _ = find_word_with_letter_list(words, w2_letters)
                if word3:
                    break
            else:
                word2 = None
    return [word1, word2, word3]


def find_word_with_letter_list(words, letters):
    word = remaining = None
    while not word:
        chosen, remaining = choose_letters_in_list(letters)
        print(f'Choosed letters {chosen}, remaining {remaining}')
        word = find_word_with_letters(words, chosen)
    return word, remaining


def choose_letters_in_list(letters, count=5):
    chosen = random.sample(letters, count)
    return chosen, [letter for letter in letters if letter not in chosen]


def find_word_with_letters(words, letters):
    for word in words:
        if set(word) == set(letters):
            return word
    else:
        return None

