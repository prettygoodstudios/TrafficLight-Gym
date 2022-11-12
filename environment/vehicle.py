from abc import abstractmethod, abstractproperty, ABC
from .constants import VehicleOrientation
from .rectangle import Rectangle

vehicleCount = 0

def getVehicleUUID():
    """Function for generating vehicle UUIDs"""
    global vehicleCount
    vehicleCount += 1
    return vehicleCount

class Vehicle(ABC):
    """Abstract class that defines the common behaviors of vehicles"""
    __slots__ = ['__vehicleUUID', '__isEnabled', '__weakref__']

    def __init__(self) -> None:
        self.__vehicleUUID = getVehicleUUID()
        self.__isEnabled = True

    def __hash__(self) -> int:
        return self.__vehicleUUID

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Vehicle):
            return False
        return self.__vehicleUUID == o.__vehicleUUID

    def __bool__(self) -> bool:
        return self.__isEnabled

    def destroy(self) -> None:
        """Used to decommission vehicle"""
        self.__isEnabled = False

    @abstractmethod
    def stop(self) -> None:
        """Requests that the vehicle stop"""

    @abstractmethod
    def go(self) -> None:
        """Requests that the vehicle start driving"""

    @abstractmethod
    def yieldToTraffic(self) -> None:
        """Requests that the vehicle yield to oncoming traffic"""

    @abstractproperty
    def velocity(self) -> tuple[float, float]:
        """Returns a tuple of the vehicle's x and y velocity"""

    @abstractproperty
    def geometry(self) -> Rectangle:
        """Returns the geometry of the vehicle"""

    @abstractproperty
    def orientation(self) -> VehicleOrientation:
        """Returns the orientation of the vehicle"""
        