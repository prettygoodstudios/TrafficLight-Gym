from environment import LightPhase
from collections import deque
from .agent import Agent
import numpy as np
from random import random, randint
             
class TDAgent(Agent):
    """Agent that uses Q-Table to learn optimal policy"""
    __slots__ = ['__qTable', '__counts', '__iterations']
    __actions = [LightPhase.EastWestGreen, LightPhase.NorthSouthGreen, LightPhase.AllRed]
    __learningRate = 0.2
    __epsilon = 0.3
    __decay = 25
    __minLearningRate = 0.01
    __discountRate = 1

    def __init__(self) -> None:
        # First index time binned into 15 slots. Each slot represents 10 discrete time steps
        # Second index is for the first yield zone cars capped to six
        # Third index is for the second yield zone cars capped to six
        # Fourth index is for the third yield zone cars capped to six
        # Fifth index is for the fourth yield zone cars capped to six
        # Sixth index is for the light phases
        self.__qTable = np.zeros(shape=(15, 6, 6, 6, 6, 3), dtype=np.float16)
        self.__iterations = 0

    def __convertStateToIndexes(self, state: tuple[tuple[int, int, int, int], int]) -> tuple[int, int, int, int, int]:
        """Converts the state into it's corresponding index in the Q-Table"""
        (yieldZoneOne, yieldZoneTwo, yieldZoneThree, yieldZoneFour), rawTime = state
        time = min([14, rawTime // 10])
        carsCanDetect = 5
        processZone = lambda cars: min(cars, carsCanDetect)
        return time, processZone(yieldZoneOne), processZone(yieldZoneTwo), processZone(yieldZoneThree), processZone(yieldZoneFour)

    def __convertActionToIndex(self, action: LightPhase) -> int:
        """Converts the state into the corresponding index in the Q-Table"""
        return self.__actions.index(action)

    def act(self, state: tuple[tuple[int, int, int, int], int]) -> LightPhase:
        def computeNewAction():
            lookupIndex = self.__convertStateToIndexes(state)
            self.__epsilon *= 0.99
            if random() < self.__epsilon:
                return self.__actions[randint(0, len(self.__actions) - 1)]
            return self.__actions[np.argmax(self.__qTable[lookupIndex])]
        newAction = computeNewAction()
        self.__iterations += 1
        return newAction

    def update(self, action: LightPhase, state: tuple[tuple[int, int, int, int], int], nextState: tuple[tuple[int, int, int, int], int], reward: int) -> None:
        stateIndex = self.__convertStateToIndexes(state)
        nextStateIndex = self.__convertStateToIndexes(nextState)
        actionIndex = (self.__convertActionToIndex(action),)
        self.__qTable[stateIndex + actionIndex] += (
            self.__learningRate *
            (
                reward
                + self.__discountRate * max(self.__qTable[nextStateIndex])
                - self.__qTable[stateIndex + actionIndex]
            )
        )

    @property
    def __learningRate(self):
        return max(
            self.__minLearningRate,
            min(1.0, 1.0 - np.log10(self.__iterations / self.__decay))
        )

    @property
    def loss(self):
        return 0
