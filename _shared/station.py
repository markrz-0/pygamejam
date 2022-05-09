from config import STATION_HEALTH, STATION_COOLDOWN, STATION_DMG

class Station:
    FREE = 0
    BLUE = 1
    RED = 2

    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.health = STATION_HEALTH
        self.last_hit = 0
        self.target = None

        self.reload_timer = STATION_COOLDOWN
        self.reloaded = True

    def reload(self, delta):
        if not self.reloaded:
            self.reload_timer -= delta

        if self.reload_timer < 0:
            self.reload_timer = STATION_COOLDOWN
            self.reloaded = True

    def shoot(self):
        self.target.health -= STATION_DMG
        self.reloaded = False

    def __str__(self):
        return f'{self.pos[0]};{self.pos[1]};{self.color}'