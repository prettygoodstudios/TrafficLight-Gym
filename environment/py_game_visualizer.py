from .visualizer import Visualizer
from .constants import LightPhase
from .rectangle import Rectangle
from .lane import Lane
import pygame

class PyGameVisualizer(Visualizer):
    """Visualization implementation using pygame"""
    __slots__ = ['__screen', '__background', '__vehicleColor', '__padding', '__scale']

    def setup(self) -> None:
        pygame.init()
        self.__padding = 10
        self.__scale = 4
        self.__screen = pygame.display.set_mode(((200 + self.__padding * 2) * self.__scale, (200 + self.__padding * 2) * self.__scale))
        self.__background = (255, 255, 255)
        self.__vehicleColor = (0, 255, 0)
        self.__laneColor = (0, 0, 0)
        self.__zoneColor = (0, 0, 255)
        

    def reset(self) -> None:
        self.__screen.fill(self.__background)

    def render(self, lanes: list[Lane], phase: LightPhase, intersection: Rectangle) -> None:
        scale = lambda x: (self.__scale * e for e in x)
        def transform(x: iter):
            x, y, width, height = x
            return x + self.__scale * self.__padding, y + self.__scale * self.__padding, width, height
        for event in pygame.event.get():
            pass
        self.__screen.fill(self.__background)

        font = pygame.font.Font('freesansbold.ttf', 15)
        # create a text surface object,
        # on which text is drawn on it.
        text = font.render(str(phase), True, self.__laneColor)
        self.__screen.blit(text, pygame.Rect(*transform(scale((5, 5, 10, 5)))))

        for lane in lanes:
            pygame.draw.rect(self.__screen, self.__laneColor, pygame.Rect(*transform(scale(lane.geometry))))
            pygame.draw.rect(self.__screen, self.__zoneColor, pygame.Rect(*transform(scale(lane.start))))
            pygame.draw.rect(self.__screen, self.__zoneColor, pygame.Rect(*transform(scale(lane.end))))
            
        pygame.draw.rect(self.__screen, self.__zoneColor, pygame.Rect(*transform(scale(intersection))))
        for lane in lanes:    
            for vehicle in lane.getVehicles(lambda x: True):
                pygame.draw.rect(self.__screen, self.__vehicleColor, pygame.Rect(*transform(scale(vehicle.geometry))))
        
        pygame.display.update()
        pygame.time.delay(50)

