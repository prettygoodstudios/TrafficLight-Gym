
from abc import abstractmethod, ABC, abstractproperty

from environment import LightPhase


class Agent(ABC):

    @abstractmethod
    def act(self, state: tuple[tuple[int, int, int, int], int]) -> LightPhase:
        """Returns the action to take given state"""

    @abstractmethod
    def update(self, action: LightPhase, state: tuple[tuple[int, int, int, int], int], reward: int) -> None:
        """Will be called, after each step. It should be used to update the agent"""

    @abstractproperty
    def loss(self):
        """Get's the loss of the agent"""
        