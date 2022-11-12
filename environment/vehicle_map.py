from math import ceil
from .vehicle import Vehicle

class VehicleMap:
    """Class that stores the space occupied by vehicles"""
    __slots__ = ['__grid', '__width', '__height']
    

    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__resetMap()

    def __resetMap(self):
        self.__grid: list[list[bool]] = [[False for _ in range(self.__height)] for _ in range(self.__width)]

    def __setOccupied(self, x: int, y: int) -> None:
        self.__grid[x][y] = True

    def isOccupied(self, x: int, y: int) -> bool:
        """Returns true if the space is occupied by a vehicle"""
        if x < 0 or y < 0:
            return False
        if x >= len(self.__grid) or y >= len(self.__grid[x]):
            return False
        return self.__grid[x][y]

    def update(self, allVehicles: list[Vehicle], reset=True):
        """Updates the map to store the latest vehicle information"""
        if reset: self.__resetMap()
        for vehicle in allVehicles:
            left, top, width, height = vehicle.geometry
            right = ceil(left + width)
            bottom = ceil(top + height)
            left = int(left)
            top = int(top)
            for x in range(max(0, left), min(right, len(self.__grid))):
                for y in range(max(0, top), min(bottom, len(self.__grid[x]))):
                    self.__setOccupied(x, y)

    def __repr__(self):
        output = ""
        for y in range(self.__height):
            for x in range(self.__width):
                output += "X" if self.isOccupied(x, y) else "_"
            output += "\n"
        return output
        