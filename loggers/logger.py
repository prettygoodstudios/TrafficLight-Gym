from abc import ABC, abstractmethod
from agents.agent import Agent
from environment import LightPhase


class Logger(ABC):

    @abstractmethod
    def logStep(self, action: LightPhase, state: tuple[tuple[int, int, int, int], int], reward: int) -> None:
        """Logs the result of taking action"""

    @abstractmethod
    def logEpisode(self, agent: Agent) -> None:
        """Logs the result of the episode"""
        