import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
import scipy

from loggers import readFromCSV

def generatePlot() -> plt.Axes:
    return plt.subplots()[1]

def renderPlot(linePlot: plt.Axes) -> None:
    plt.style.use('./plots.mplstyle')
    linePlot.set_xlabel('Episode', fontsize=20)
    linePlot.set_ylabel('Reward', fontsize=20)
    linePlot.set_title('Learning Curve')
    # linePlot.set_yticks(range(*map(int, linePlot.get_ylim()), 100000))
    # linePlot.set_xticks(range(*map(int, linePlot.get_xlim()), 10))
    plt.legend()
    plt.show()

def smooth(scalars: list[float], weight: float) -> list[float]:  # Weight between 0 and 1
    last = scalars[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in scalars:
        smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
        smoothed.append(smoothed_val)                        # Save it
        last = smoothed_val                                  # Anchor the last smoothed value
        
    return smoothed  


def plotSeries(data: list[tuple[float, float]], label: str, linePlot: plt.Axes) -> None:
    """Plots a series of rewards"""
    _, rewards = zip(*data)
    episodes = range(len(rewards))
    linePlot.plot(episodes, smooth(rewards, 0.95), label=label)

    # Fit with polyfit
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(episodes, rewards)
    linePlot.plot(episodes, (intercept + slope * np.array(episodes)), '-', label=f"{label} best fit: y = {round(intercept, 2)} + {round(slope, 2)}x, r^2={round(r_value, 2)}, p={round(p_value, 2)}, std-err={round(std_err, 2)}")

def main():
    linePlot = generatePlot()
    directory = './data/'
    with open(f"{directory}q-table-episodes.csv", 'r') as file:
        plotSeries(readFromCSV(file), 'Temporal Difference', linePlot)
    # with open(f"{directory}random-episodes.csv", 'r') as file:
    #     plotSeries(readFromCSV(file), 'Random', linePlot)
    with open(f"{directory}sequential-episodes.csv", 'r') as file:
        plotSeries(readFromCSV(file), 'Sequential', linePlot)
    renderPlot(linePlot)

if __name__ == "__main__":
    main()
