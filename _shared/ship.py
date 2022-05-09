
healths = [
    10, # fighter
    50 # carrier
]

speeds = [
    0.04,
    0.025
]

ranges = [
    50,
    100
]

# (health, speed_motifier, range, cooldown (in ms), dmg)
consts = [
    (10, 0.04, 150, 500, 10),
    (50, 0.06, 200, 1000, 15)
]

class Ship:
    FIGHTER = 0
    CARRIER = 1

    def __init__(self, pos, ship_type, color):
        self.pos = pos
        self.ship_type = ship_type
        self.color = color # 1 - blue; 2 - red
        self.health, self.speed, self.range, self.cooldown, self.dmg = consts[ship_type]
        self.reload_timer = self.cooldown
        self.reloaded = True

    def reload(self, delta):
        if not self.reloaded:
            self.reload_timer -= delta

        if self.reload_timer < 0:
            self.reload_timer = self.cooldown
            self.reloaded = True

    def shoot(self):
        self.reloaded = False

    def __str__(self):
        return f'{self.pos[0]};{self.pos[1]};{self.ship_type};{self.color}'