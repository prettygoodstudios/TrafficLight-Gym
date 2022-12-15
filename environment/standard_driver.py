from typing import Union
import weakref
from .driving_strategy import DrivingStrategy
from .constants import VehicleOrientation
from .vehicle import Vehicle
from .rectangle import Rectangle

class StandardDriver(DrivingStrategy):
    """Most basic driving strategy"""
    __slots__ = ['__maxVelocity', '__acceleration', '__vehicleAhead', '__vehicle', '__intersection']

    __orientationAccelerations = {
        VehicleOrientation.North: (0, -1),
        VehicleOrientation.South: (0, 1),
        VehicleOrientation.West: (-1, 0),
        VehicleOrientation.East: (1, 0),
    }

    def __init__(self, maxVelocity: float, acceleration: float, brakeAcceleration: float, vehicle: Vehicle, vehicleAhead: Union[Vehicle, None], intersection: Rectangle) -> None:
        self.__maxVelocity = maxVelocity
        self.__acceleration = acceleration
        self.__brakeAcceleration = brakeAcceleration
        self.__vehicle = vehicle
        self.__vehicleAhead = weakref.ref(vehicleAhead) if vehicleAhead else None
        self.__intersection = intersection

    def __handleStopping(self) -> Union[None, tuple[float, float]]:
        vehicleAhead = self.__vehicleAhead() if self.__vehicleAhead else None
        if not vehicleAhead:
            return None
        distance = self.__vehicle.geometry.minDistance(vehicleAhead.geometry)
        vehicleLength = max(tuple(self.__vehicle.geometry)[2:])
        if distance < vehicleLength * 2:
            return self.__stop(self.__acceleration * 3)

    def move(self) -> tuple[float, float]:
        return self.__move(1)

    def __move(self, scaleFactor) -> tuple[float, float]:
        stop = self.__handleStopping()
        if stop:
            return stop
        velocityX, velocityY = self.__vehicle.velocity
        if (velocityX ** 2 + velocityY ** 2) ** 0.5 > self.__maxVelocity:
            return self.__vehicle.velocity
        xShare, yShare = self.__orientationAccelerations[self.__vehicle.orientation]
        return scaleFactor * xShare * self.__acceleration + velocityX, scaleFactor * yShare * self.__acceleration + velocityY

    def stop(self) -> tuple[float, float]:
        stop = self.__handleStopping()
        if stop:
            return stop
        velocityX, velocityY = self.__vehicle.velocity
        magnitude = abs(velocityX + velocityY) 
        if magnitude < self.__maxVelocity * 0.2 and self.__vehicle.geometry.minDistance(self.__intersection) > 5:
            return self.__move(0.1)
        if self.__vehicle.geometry.intersects(self.__intersection):
            return self.__move(-0.1)
        return self.__stop(self.__brakeAcceleration)

    def __stop(self, acceleration: float) -> tuple[float, float]:
        velocityX, velocityY = self.__vehicle.velocity
        xShare, yShare = self.__orientationAccelerations[self.__vehicle.orientation]
        if abs(velocityX) < abs(acceleration * xShare) or abs(velocityY) < abs(acceleration * yShare):
            return (0, 0)
        directionX = 1 if (velocityX > 0 and xShare > 0) or (velocityX < 0 and xShare < 0) else -1
        directionY = 1 if (velocityY > 0 and yShare > 0) or (velocityY < 0 and yShare < 0) else -1
        return (velocityX - acceleration * xShare * directionX, velocityY - acceleration * yShare * directionY)
        
    def yieldToTraffic(self) -> tuple[float, float]:
        return self.__vehicle.velocity
