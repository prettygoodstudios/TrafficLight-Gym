
from typing_extensions import Self


class Rectangle:
    """Class for representing rectangular geometries"""
    __slots__ = ['__dimensions', '__position']

    def __init__(self, dimensions: tuple[float, float], position: tuple[float, float]) -> None:
        self.__dimensions = dimensions
        self.__position = position

    def intersects(self, other: Self) -> bool:
        """Checks if rectangle intersects other rectangle"""
        myX, myY, myWidth, myHeight = self
        otherX, otherY, otherWidth, otherHeight = other

        # If rectangles are to the side of each other
        if myX + myWidth < otherX or otherX + otherWidth < myX:
            return False

        # If rectangles are above or below each other
        if myY + myHeight < otherY or otherY + otherHeight < myY:
            return False

        # Otherwise they overlap
        return True

    def corners(self) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
        x, y, width, height = self
        return ((x,y), (x + width, y), (x, y + height), (x + width, y + height))

    def minDistance(self, other: Self) -> float:
        myCorners = self.corners()
        otherCorners = other.corners()
        minDistance = None
        for x, y in myCorners:
            for otherX, otherY in otherCorners:
                distance = ((x - otherX) ** 2 + (y - otherY) ** 2) ** 0.5
                minDistance = min((distance if minDistance is None else minDistance), distance)
        return minDistance

    @property
    def position(self):
        """Returns x,y""" 
        return self.__position

    @property
    def dimensions(self):
        """Returns width, height"""
        return self.__dimensions

    def __iter__(self):
        """Iterating through rectangle yields x, y, width, height"""
        for val in (*self.__position, *self.dimensions):
            yield val