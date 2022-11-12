from abc import ABC, abstractmethod
from .lane import Lane
from .rectangle import Rectangle
from .constants import LightPhase

class Visualizer(ABC):
    """Protocol for visualizations implementations"""

    @abstractmethod
    def setup(self) -> None:
        """Setups the visualization"""

    @abstractmethod
    def reset(self) -> None:
        """Resets the visualization"""

    @abstractmethod
    def render(self, lanes: list[Lane], phase: LightPhase, intersection: Rectangle) -> None:
        """Renders the simulation"""
