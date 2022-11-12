from .agent import Agent
from environment import LightPhase

class SequentialAgent(Agent):
    """Rotates through phrases at the interval"""
    __slots__ = ['__frame', '__phaseIndex', '__interval']
    __phases = [LightPhase.NorthSouthGreen, LightPhase.AllRed, LightPhase.EastWestGreen]

    def __init__(self, interval: int) -> None:
        self.__frame = 0
        self.__phaseIndex = 0
        self.__interval = interval

    def act(self, state: tuple[tuple[int, int, int, int], int]) -> LightPhase:
        return self.__phases[self.__phaseIndex % len(self.__phases)]

    def update(self, action: LightPhase, state: tuple[tuple[int, int, int, int], int], reward: int) -> None:
        self.__frame += 1
        if self.__frame % self.__interval == 0:
            self.__phaseIndex += 1

    @property
    def loss(self):
        return 0
