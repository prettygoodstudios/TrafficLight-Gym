from random import randint
from .car import Car
from .lane import Lane
from .vehicle import VehicleOrientation, Vehicle
from .vehicle_map import VehicleMap
from .rectangle import Rectangle
from .visualizer import Visualizer
from .constants import LightPhase

class Intersection:
    __slots__ = ['__lanes', '__geometry', '__yieldZones', '__vehicleMap', '__visualizer', '__phase', '__phaseCount']

    def __init__(self, visualizer: Visualizer = None) -> None:
        self.__lanes = [
            Lane(VehicleOrientation.North, Rectangle((4, 200), (101, 0)), Rectangle((4, 3), (101, 200)), Rectangle((4, 3), (101, -3))),
            Lane(VehicleOrientation.South, Rectangle((4, 200), (95, 0)), Rectangle((4, 3), (95, -3)), Rectangle((4, 3), (95, 200))),
            Lane(VehicleOrientation.West, Rectangle((200, 4), (0, 95)), Rectangle((3, 4), (200, 95)), Rectangle((3, 4), (0, 95))),
            Lane(VehicleOrientation.East, Rectangle((200, 4), (0, 101)), Rectangle((3, 4), (0, 101)), Rectangle((3, 4), (200, 101))),
        ]
        self.__vehicleMap = VehicleMap(200, 200)
        self.__geometry = Rectangle((10, 10), (95, 95))
        self.__yieldZones = {
            LightPhase.EastWestGreen: [
                Rectangle((4, 20), (101, 105)),
                Rectangle((4, 20), (95, 75)),
            ],
            LightPhase.NorthSouthGreen: [
                Rectangle((20, 4), (75, 101)),
                Rectangle((20, 4), (105, 95)),
            ],
            LightPhase.AllRed: [
                Rectangle((20, 4), (75, 101)),
                Rectangle((20, 4), (105, 95)),
                Rectangle((4, 20), (101, 105)),
                Rectangle((4, 20), (95, 75)),
            ],
        }
        self.__phase = None
        self.__phaseCount = 0
        self.__visualizer = visualizer
        if visualizer:
            visualizer.setup()

    def getTotalIdleTime(self) -> int:
        """Returns the idle time of all of the vehicles in the intersection"""
        return sum([sum([vehicle.idleTime for vehicle in lane.getVehicles()]) for lane in self.__lanes])

    def getVehiclesWithinIntersection(self) -> list[Vehicle]:
        """Returns a list of the vehicles currently traveling in the intersection"""
        vehicles = []
        for lane in self.__lanes:
            vehicles.extend(lane.getVehiclesInGeometry(self.__geometry))
        return vehicles

    def getVehiclesWithinYieldZones(self):
        """Returns a list of lists that contain the vehicles within each yield zone"""
        vehicles: list[Vehicle] = []
        zones = self.__yieldZones[LightPhase.AllRed]
        for zone in zones:
            vehicles.append([])
            for lane in self.__lanes:
                vehicles[-1].extend(lane.getVehiclesInGeometry(zone))
        return vehicles

    def removeVehicle(self, vehicle: Vehicle):
        for lane in self.__lanes:
            lane.removeVehicle(vehicle)

    def update(self, phase: LightPhase):
        """Updates the intersection at each discrete time step"""
        if phase == self.__phase:
            self.__phaseCount += 1
        else:
            self.__phaseCount = 0
        self.__phase = phase
        self.__vehicleMap.update([], reset=True)
        for lane in self.__lanes:
            vehiclesToStop: set[Vehicle] = set()
            lane.update(self.__vehicleMap)
            for yieldZone in self.__yieldZones[phase]:
                vehiclesToStop.update(lane.getVehiclesInGeometry(yieldZone))
            for vehicle in vehiclesToStop:
                vehicle.stop()
            for vehicle in filter(lambda v: not v in vehiclesToStop, lane.getVehicles(lambda _: True)):
                vehicle.go()
            
            startX, startY, *_ = lane.start 
            clearToAddVehicle = not lane.getLastVehicle() or lane.getLastVehicle().geometry.minDistance(lane.start) > 5
            
            if clearToAddVehicle and randint(1, 100) < 10:
                lane.addVehicle(Car(startX + 1, startY + 1, lane.orientation, lane.getLastVehicle(), self.__geometry))

    def render(self):
        """Visualizes intersection, if visualizer provided"""
        if self.__visualizer:
            self.__visualizer.render(self.__lanes, self.__phase, self.__geometry, self.__vehicleMap)

    def __repr__(self) -> str:
        output = ""
        width, height = 220, 220
        padding = 10
        for row in range(height):
            y = row - padding
            for col in range(width):
                cell = ' '
                x = col - padding
                position = Rectangle((1, 1), (x, y))
                for lane in self.__lanes:
                    if lane.geometry.intersects(position):
                        cell = 'L'
                    if lane.start.intersects(position):
                        cell = 'S'
                    if lane.end.intersects(position):
                        cell = 'E'
                    if self.__geometry.intersects(position):
                        cell = 'I'
                if self.__vehicleMap.isOccupied(x, y):
                    cell = 'V'
                output += cell
            output += '\n'
        return output

    @property
    def phaseCount(self):
        return self.__phaseCount

