from .rectangle import Rectangle
from .car import Car
from .constants import VehicleOrientation
from .vehicle_map import VehicleMap
from .vehicle import Vehicle

def testVehicleMap():
    map = VehicleMap(10, 10)
    vehicles: list[Vehicle] = [
        Car(2, 2, VehicleOrientation.North, map), 
        Car(9, 9, VehicleOrientation.North, map), 
        Car(-1, -1, VehicleOrientation.North, map),
        Car(0, 5, VehicleOrientation.East, map),
    ]
    map.update(vehicles)
    print(map)
    assert str(map) == """X_________
X_________
__XX______
__XX______
__XX______
XXX_______
XXX_______
__________
__________
_________X
"""
    map.update([])
    print(map)
    assert str(map) == """__________
__________
__________
__________
__________
__________
__________
__________
__________
__________
"""
    print("Passed vehicle map tests!!!")

def testRectangleIntersection():
    rectOne = Rectangle((10, 10), (0, 0))
    assert rectOne.intersects(Rectangle((30,30), (3, 3)))
    assert rectOne.intersects(Rectangle((1, 1), (3, 3)))
    rectTwo = Rectangle((3, 2), (201, 96))
    assert rectTwo.intersects(Rectangle((3, 4), (200, 95)))

    print("Passed rectangle intersection tests!!!")

def main():
    testVehicleMap()
    testRectangleIntersection()

if __name__ == '__main__':
    main()
