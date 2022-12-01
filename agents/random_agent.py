from random import randint
from .agent import Agent
from environment import LightPhase

class RandomAgent(Agent):
    __slots__ = ['__frame', '__phase']

    def __init__(self) -> None:
        self.__frame = 0
        self.__phase = self.__getRandomPhase()

    def __getRandomPhase(self) -> LightPhase:
        return [LightPhase.NorthSouthGreen, LightPhase.EastWestGreen, LightPhase.AllRed][randint(0, 2)]

    def act(self, state: tuple[tuple[int, int, int, int], int]) -> LightPhase:
        return self.__phase
 
    def update(self, action: LightPhase, state: tuple[tuple[int, int, int, int], int], reward: int) -> None:
        self.__frame += 1
        if self.__frame % 20 == 0:
            self.__phase = self.__getRandomPhase()

    @property
    def loss(self):
        return 0