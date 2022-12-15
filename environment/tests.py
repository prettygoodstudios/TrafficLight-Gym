from .rectangle import Rectangle
from .car import Car
from .constants import VehicleOrientation
from .vehicle import Vehicle


def testRectangleIntersection():
    rectOne = Rectangle((10, 10), (0, 0))
    assert rectOne.intersects(Rectangle((30,30), (3, 3)))
    assert rectOne.intersects(Rectangle((1, 1), (3, 3)))
    rectTwo = Rectangle((3, 2), (201, 96))
    assert rectTwo.intersects(Rectangle((3, 4), (200, 95)))

    print("Passed rectangle intersection tests!!!")

def main():
    testRectangleIntersection()

if __name__ == '__main__':
    main()
