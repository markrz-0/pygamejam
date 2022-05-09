from config import STATION_HEALTH

class Station:
    FREE = 0
    BLUE = 1
    RED = 2

    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.health = STATION_HEALTH

    def __str__(self):
        return f'{self.pos[0]};{self.pos[1]};{self.color}'