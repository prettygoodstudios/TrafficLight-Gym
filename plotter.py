import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
import scipy

from loggers import readFromCSV

def generatePlot() -> plt.Axes:
    return plt.subplots()[1]

def renderPlot(linePlot: plt.Axes) -> None:
    plt.style.use('_mpl-gallery')
    linePlot.set_xlabel('Episode')
    linePlot.set_ylabel('Reward')
    linePlot.set_title('Learning curves')
    # linePlot.set_yticks(range(*map(int, linePlot.get_ylim()), 100000))
    # linePlot.set_xticks(range(*map(int, linePlot.get_xlim()), 10))
    plt.legend()
    plt.show()
    


def plotSeries(data: list[tuple[float, float]], label: str, linePlot: plt.Axes) -> None:
    """Plots a series of rewards"""
    _, rewards = zip(*data)
    episodes = range(len(rewards))
    linePlot.plot(episodes, rewards, label=label)

    # Fit with polyfit
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(episodes, rewards)
    linePlot.plot(episodes, (intercept + slope * np.array(episodes)), '-', label=f"{label} best fit: y = {round(intercept, 2)} + {round(slope, 2)}x, r^2={r_value}, p={p_value}, std-err={std_err}")

def main():
    linePlot = generatePlot()
    directory = './data/'
    with open(f"{directory}q-table-episodes.csv", 'r') as file:
        plotSeries(readFromCSV(file), 'Q-Table', linePlot)
    with open(f"{directory}random-episodes.csv", 'r') as file:
        plotSeries(readFromCSV(file), 'Random', linePlot)
    with open(f"{directory}sequential-episodes.csv", 'r') as file:
        plotSeries(readFromCSV(file), 'Sequential', linePlot)
    renderPlot(linePlot)

if __name__ == "__main__":
    main()
