from config import STATION_HEALTH

class Stations:
    FREE = 0
    BLUE = 1
    RED = 2

    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.health = STATION_HEALTH

    def to_bytes(self):
        return f'{self.pos[0]};{self.pos[1]}'