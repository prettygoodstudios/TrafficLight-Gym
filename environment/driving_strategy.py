
from abc import ABC, abstractmethod

class DrivingStrategy(ABC):
    """Abstract class that defines a strategy for driving a vehicle"""

    @abstractmethod
    def move(self) -> tuple[float, float]:
        """Handles moving the vehicle. Returns vehicle new velocity."""

    @abstractmethod
    def yieldToTraffic(self) -> tuple[float, float]:
        """Handles yielding to traffic. Returns vehicle new velocity."""

    @abstractmethod
    def stop(self) -> tuple[float, float]:
        """Handles stopping the vehicle and keeping it stationary. Returns new velocity."""

