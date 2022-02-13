from matplotlib import pyplot as plt
import pandas as pd

from agent import ArianeAgent, InputAgent
from env import Env
import logging


def main():
    env = Env()
    agent = ArianeAgent(env)
    play(env, agent)


def play(env, agent):
    logging.basicConfig(level=logging.INFO)
    game(env, agent)


def game(env, agent):
    env.reset()
    agent.reset()
    terminal = False
    while not terminal:
        word = agent.act()
        matches, terminal = env.step(word)
        if not terminal:
            agent.observe(word, matches)
    return env.steps


def analyse(env, agent, num_games=1000):
    df = pd.DataFrame.from_records({"steps": [game(env, agent) for _ in range(num_games)]})
    print(df.describe())
    df.plot.hist(density=1, bins=env.NUM_TRIES+1, range=(0.5, env.NUM_TRIES+1.5)).set_title(agent.__class__.__name__)
    plt.show()


if __name__ == '__main__':
    main()
