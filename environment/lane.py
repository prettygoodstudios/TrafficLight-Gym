from collections import deque
from typing import Union
from .vehicle import Vehicle, VehicleOrientation
from .vehicle_map import VehicleMap
from .rectangle import Rectangle

class Lane:
    __slots__ = ['__vehicles', '__orientation', '__geometry', '__start', '__end']

    def __init__(self, orientation: VehicleOrientation, geometry: Rectangle, start: Rectangle, end: Rectangle) -> None:
        self.__orientation = orientation
        self.__vehicles: deque[Vehicle] = deque()
        self.__geometry = geometry
        self.__start = start
        self.__end = end

    def addVehicle(self, vehicle: Vehicle) -> None:
        """Adds vehicle to lane"""
        self.__vehicles.append(vehicle)
 
    def getVehiclesInGeometry(self, geometry: Rectangle) -> iter:
        """Gets an iterable of the vehicles intersecting the provided geometry"""
        return self.getVehicles(lambda v: geometry.intersects(v.geometry))

    def getVehicles(self, filterer: callable) -> iter:
        """Gets an iterable of the vehicles that satisfy the filterer's conditions"""
        return filter(filterer, self.__vehicles)

    def getLastVehicle(self) -> Union[Vehicle, None]:
        """Gets the last vehicle added to lane"""
        if len(self.__vehicles) == 0:
            return None
        return self.__vehicles[-1]
        
    def removeVehicle(self, vehicle: Vehicle):
        if vehicle in self.__vehicles:
            self.__vehicles.remove(vehicle)
            vehicle.destroy()

    def update(self, vehicleMap: VehicleMap):
        """Used to update lane at each discrete time step"""
        if len(self.__vehicles) > 0 and self.__vehicles[0].geometry.intersects(self.__end):
            self.__vehicles.popleft().destroy()
        vehicleMap.update(list(self.__vehicles), False)

    @property
    def start(self) -> Rectangle:
        return self.__start

    @property
    def end(self) -> Rectangle:
        return self.__end

    @property
    def geometry(self) -> Rectangle:
        return self.__geometry

    @property
    def orientation(self) -> VehicleOrientation:
        return self.__orientation
