from io import TextIOWrapper
from environment import Environment
from runner import runner
from loggers import CSVLogger
from agents import RandomAgent, SequentialAgent, Agent, QTableAgent

def runTrials(output: TextIOWrapper, agent: Agent, trials: int = 100):
    logger = CSVLogger(output)
    for _ in range(trials):
        runner(Environment(), agent, logger)

def main():
    with open("./data/random-episodes.csv", "w") as file:
        runTrials(file, RandomAgent())
    with open("./data/sequential-episodes.csv", "w") as file:
        runTrials(file, SequentialAgent(40))
    with open("./data/q-table-episodes.csv", "w") as file:
        runTrials(file, QTableAgent())

if __name__ == '__main__':
    main()
