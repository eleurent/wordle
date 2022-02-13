# encoding: utf-8
from agent import ArianeAgent, InputAgent
from env import Env
import logging

logging.basicConfig(level=logging.INFO)


def main():
    env = Env()
    agent = ArianeAgent(env)
    terminal = False
    while not terminal:
        word = agent.act()
        matches, terminal = env.step(word)
        if not terminal:
            agent.observe(word, matches)


if __name__ == '__main__':
    main()
