from io import TextIOWrapper
from .logger import Logger
from environment import Environment, LightPhase
from agents.agent import Agent

class CSVLogger(Logger):
    """Logger that logs results to CSV format"""
    __slots__ = ['__fileHandle', '__cumulativeReward']

    def __init__(self, file: TextIOWrapper) -> None:
        self.__cumulativeReward = 0
        self.__fileHandle = file
        self.__printHeaders()

    def __printHeaders(self):
        print("Loss, Reward", file=self.__fileHandle)

    def logStep(self, action: LightPhase, state: tuple[tuple[int, int, int], int], reward: int) -> None:
        self.__cumulativeReward += reward

    def logEpisode(self, agent: Agent) -> None:
        cumulativeReward = self.__cumulativeReward
        self.__cumulativeReward = 0
        print(f"{agent.loss}, {cumulativeReward}", file=self.__fileHandle)