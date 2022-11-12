from .logger import Logger
from environment import LightPhase
from agents.agent import Agent

class ConsoleLogger(Logger):
    """Logger that logs results to console"""
    __slots__ = ['__cumulativeReward']

    def __init__(self) -> None:
        self.__cumulativeReward = 0

    def logStep(self, action: LightPhase, state: tuple[tuple[int, int, int], int], reward: int) -> None:
        self.__cumulativeReward += reward
        print(f"Action: {action}, State: {state}, Reward: {reward}")

    def logEpisode(self, agent: Agent) -> None:
        cumulativeReward = self.__cumulativeReward
        self.__cumulativeReward = 0
        print(f"Loss: {agent.loss}, Cumulative Reward: {cumulativeReward}")
