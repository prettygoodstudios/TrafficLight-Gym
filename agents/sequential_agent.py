from .agent import Agent
from environment import LightPhase

class SequentialAgent(Agent):
    """Rotates through phrases at the specified timings"""
    __slots__ = ['__frame', '__phaseIndex']
    __phases = [LightPhase.NorthSouthGreen, LightPhase.AllRed, LightPhase.EastWestGreen]
    __timings = [4, 1.5, 4]

    def __init__(self) -> None:
        self.__frame = 0
        self.__phaseIndex = 0

    def act(self, state: tuple[tuple[int, int, int, int], int]) -> LightPhase:
        return self.__phases[self.__phaseIndex % len(self.__phases)]

    def update(self, action: LightPhase, state: tuple[tuple[int, int, int, int], int], nextState: tuple[tuple[int, int, int, int], int], reward: int) -> None:
        self.__frame += 1
        if self.__frame == self.__timings[self.__phaseIndex % len(self.__phases)]:
            self.__phaseIndex += 1
            self.__frame = 0

    @property
    def loss(self):
        return 0
