from io import TextIOWrapper
from environment import Environment, PyGameVisualizer
from runner import runner
from loggers import CSVLogger, ConsoleLogger
from agents import RandomAgent, SequentialAgent, Agent, QTableAgent, TDAgent
from sys import argv

def runTrials(output: TextIOWrapper, agent: Agent, trials, visualize=False):
    logger = ConsoleLogger() if visualize else CSVLogger(output)
    for t in range(trials):
        runner(Environment(PyGameVisualizer() if visualize else None), agent, logger, 500, 10)
        if not visualize:
            print(f"Trial: {t}")

def main():
    visualize = '-v' in argv
    if '-t' in argv and argv.index('-t') < len(argv) - 1:
        trials = int(argv[argv.index('-t') + 1])
    else:
        trials = 100
    with open("./data/q-table-episodes.csv", "w", ) as file:
        runTrials(file, TDAgent(), trials=trials, visualize=visualize)
    with open("./data/random-episodes.csv", "w") as file:
        runTrials(file, RandomAgent(), trials=trials, visualize=visualize)
    with open("./data/sequential-episodes.csv", "w") as file:
        runTrials(file, SequentialAgent(), trials=trials, visualize=visualize)

if __name__ == '__main__':
    main()
