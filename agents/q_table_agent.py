from environment import LightPhase
from .agent import Agent
import numpy as np
from random import random, randint

class QTableAgent(Agent):
    """Agent that uses Q-Table to learn optimal policy"""
    __slots__ = ['__qTable']
    __actions = [LightPhase.EastWestGreen, LightPhase.NorthSouthGreen, LightPhase.AllRed]
    __learningRate = 0.1
    __epsilon = 0.1

    def __init__(self) -> None:
        # First index time binned into 15 slots. Each slot represents 10 discrete time steps
        # Second index is for the first yield zone cars capped to three
        # Third index is for the second yield zone cars capped to three
        # Fourth index is for the third yield zone cars capped to three
        # Fifth index is for the fourth yield zone cars capped to three
        # Sixth index is for the light phases
        self.__qTable = np.array(15, 4, 4, 4, 3, dtype=np.ubyte) + 2

    def __convertStateToIndexes(self, state: tuple[tuple[int, int, int, int], int]) -> tuple[int, int, int, int, int]:
        """Converts the state into it's corresponding index in the Q-Table"""
        (yieldZoneOne, yieldZoneTwo, yieldZoneThree, yieldZoneFour), rawTime = state
        time = min([14, rawTime // 10])
        return time, yieldZoneOne, yieldZoneTwo, yieldZoneThree, yieldZoneFour 

    def __convertActionToIndex(self, action: LightPhase) -> np.ubyte:
        """Converts the state into the corresponding index in the Q-Table"""
        return self.__actions.index(action)

    def act(self, state: tuple[tuple[int, int, int, int], int]) -> LightPhase:
        lookupIndex = self.__qTable[self.__convertStateToIndexes(state)]
        if random() < self.__epsilon:
            return self.__qTable[lookupIndex + (randint(0, len(self.__qTable[lookupIndex]) - 1),)]
        return np.argmax(self.__qTable[lookupIndex])

    def update(self, action: LightPhase, state: tuple[tuple[int, int, int, int], int], reward: int) -> None:
        lookupIndex = self.__convertStateToIndexes(state) + self.__convertActionToIndex(action)
        self.__qTable[lookupIndex] += self.__learningRate * (reward - self.__qTable[lookupIndex])
        
    @property
    def loss(self):
        return 0
