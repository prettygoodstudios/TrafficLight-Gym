from typing import Union

from .rectangle import Rectangle
from .standard_driver import StandardDriver
from .vehicle import Vehicle, VehicleOrientation


class Car(Vehicle):
    __slots__ = ['__velocity', '__geometry', '__orientation', '__strategy', '__idleTime']

    def __init__(self, x: int, y: int, orientation: VehicleOrientation, vehicleAhead: Union[Vehicle, None], intersection: Rectangle):
        super().__init__()
        self.__velocity = (0, 0)
        self.__orientation = orientation
        dimensions = (2, 3) if orientation in {VehicleOrientation.North, VehicleOrientation.South} else (3, 2)
        self.__geometry = Rectangle(dimensions, (x, y))
        self.__strategy = StandardDriver(2, 1, 0.25, self, vehicleAhead, intersection)
        self.__idleTime = 0

    def __updatePosition(self) -> None:
        velocityX, velocityY = self.__velocity
        x, y, *_ = self.__geometry
        self.__geometry = Rectangle(self.__geometry.dimensions, (x + velocityX, y + velocityY))
        if velocityX + velocityY == 0:
            self.__idleTime += 1

    def go(self) -> None:
        self.__velocity = self.__strategy.move()
        self.__updatePosition()

    def stop(self) -> None:
        self.__velocity = self.__strategy.stop()
        self.__updatePosition()

    def yieldToTraffic(self) -> None:
        self.__velocity = self.__strategy.yieldToTraffic()
        self.__updatePosition()

    @property
    def velocity(self) -> tuple[float, float]:
        return self.__velocity

    @property
    def geometry(self) -> Rectangle:
        return self.__geometry

    @property
    def idleTime(self) -> int:
        return self.__idleTime

    @property
    def orientation(self) -> VehicleOrientation:
        return self.__orientation

    def __repr__(self) -> str:
        return f"Car(UUID={hash(self)}, Velocity={self.__velocity}, Orientation={self.__orientation})"
