# encoding: utf-8
from agent import letter_counts, most_frequent_letters, Agent
from env import game, Env


def main():
    env = Env()
    agent = Agent(env)
    for _ in range(6):
        terminal = agent.act()
        if terminal:
            break

    # game(env.answers, env.allowed)


if __name__ == '__main__':
    main()
