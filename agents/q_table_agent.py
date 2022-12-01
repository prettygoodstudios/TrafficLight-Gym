from environment import LightPhase
from collections import deque
from .agent import Agent
import numpy as np
from random import random, randint

def callOnePerNCalls(perCalls: int):
    """Decorator that only calls decorated function every n calls. It will return what the decorated function last returned."""
    def decorator(func: callable):
        calls = 0
        remembered = None
        def wrapper(*args, **kwargs):
            nonlocal calls
            nonlocal remembered
            if calls % perCalls == 0:
                remembered = func(*args, *kwargs)
            calls += 1   
            return remembered
        return wrapper
    return decorator
             
class QTableAgent(Agent):
    """Agent that uses Q-Table to learn optimal policy"""
    __slots__ = ['__qTable', '__previousAction', '__flipped']
    __actions = [LightPhase.EastWestGreen, LightPhase.NorthSouthGreen]
    __learningRate = 0.2
    __epsilon = 0.04
    __yieldDuration = 10

    def __init__(self) -> None:
        # First index time binned into 15 slots. Each slot represents 10 discrete time steps
        # Second index is for the first yield zone cars capped to six
        # Third index is for the second yield zone cars capped to six
        # Fourth index is for the third yield zone cars capped to six
        # Fifth index is for the fourth yield zone cars capped to six
        # Sixth index is for the light phases
        self.__qTable = np.zeros(shape=(15, 6, 6, 6, 6, 2), dtype=np.float16)
        self.__previousAction = LightPhase.EastWestGreen
        self.__flipped = 0

    def __convertStateToIndexes(self, state: tuple[tuple[int, int, int, int], int]) -> tuple[int, int, int, int, int]:
        """Converts the state into it's corresponding index in the Q-Table"""
        (yieldZoneOne, yieldZoneTwo, yieldZoneThree, yieldZoneFour), rawTime = state
        time = min([14, rawTime // 10])
        return time, yieldZoneOne, yieldZoneTwo, yieldZoneThree, yieldZoneFour 

    def __convertActionToIndex(self, action: LightPhase) -> int:
        """Converts the state into the corresponding index in the Q-Table"""
        return self.__actions.index(action)

    def act(self, state: tuple[tuple[int, int, int, int], int]) -> LightPhase:
        if self.__flipped:
            return LightPhase.AllRed
        def computeNewAction():
            lookupIndex = self.__convertStateToIndexes(state)
            self.__epsilon *= 0.99
            if random() < self.__epsilon:
                return self.__actions[randint(0, len(self.__actions) - 1)]
            return self.__actions[np.argmax(self.__qTable[lookupIndex])]
        newAction = computeNewAction()
        if newAction == self.__previousAction:
            return self.__previousAction
        self.__previousAction = newAction
        self.__flipped = self.__yieldDuration
        return LightPhase.AllRed

    def update(self, action: LightPhase, state: tuple[tuple[int, int, int, int], int], reward: int) -> None:
        if self.__flipped:
            self.__flipped -= 1
            return
        lookupIndex = self.__convertStateToIndexes(state) + (self.__convertActionToIndex(action),)
        self.__qTable[lookupIndex] += self.__learningRate * (reward - self.__qTable[lookupIndex])

    @property
    def loss(self):
        return 0
