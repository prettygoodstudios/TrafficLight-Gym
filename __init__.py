from random import randint
from environment import Environment, LightPhase

def main():
    environment = Environment()
    frame = 1
    phase = LightPhase.NorthSouthGreen
    while True:
        if frame % 50 == 0:
            phase = [LightPhase.NorthSouthGreen, LightPhase.EastWestGreen, LightPhase.AllRed][randint(0, 2)]
        print(environment.step(phase))
        environment.render()
        frame += 1

if __name__ == '__main__':
    main()
