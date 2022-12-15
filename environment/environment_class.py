from .visualizer import Visualizer
from .intersection import Intersection
from .constants import LightPhase

class Environment:
    __slots__ = ['__intersection', '__crashes']

    def __init__(self, visualizer: Visualizer = None) -> None:
        self.__intersection = Intersection(visualizer)
        self.__crashes = 0

    def __computeReward(self):
        intersectionVehicles = self.__intersection.getVehiclesWithinIntersection()
        crashes = 0

        for i, vehicle in enumerate(intersectionVehicles):
            for j in range(i+1, len(intersectionVehicles)):
                vehicleTwo = intersectionVehicles[j]
                if vehicle.geometry.intersects(vehicleTwo.geometry):
                    crashes += 1
                    self.__crashes += 1
                    self.__intersection.removeVehicle(vehicle)
                    self.__intersection.removeVehicle(vehicleTwo)
        
        return -self.__intersection.getTotalIdleTime() - crashes * 10000

    @property
    def state(self) -> tuple[tuple[int, int, int, int], int]:
        return ([len(zone) for zone in self.__intersection.getVehiclesWithinYieldZones()], self.__intersection.phaseCount)

    def step(self, action: LightPhase):
        """Environment's step function returns state, reward and done status"""
        self.__intersection.update(action)
        reward = self.__computeReward()
        return self.state, reward, False

    def render(self):
        """Environment's render function"""
        self.__intersection.render()

    def reset(self):
        """Reset's the environment"""
        self.__intersection = Intersection()
        self.__crashes = 0
