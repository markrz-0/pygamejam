
healths = [
    10, # fighter
    50 # carrier
]

speeds = [
    0.04,
    0.025
]

class Ship:
    FIGHTER = 0
    CARRIER = 1

    def __init__(self, pos, ship_type, color):
        self.pos = pos
        self.ship_type = ship_type
        self.color = color # 1 - blue; 2 - red
        self.health = healths[ship_type]
        self.speed = speeds[ship_type]

    def __str__(self):
        return f'{self.pos[0]};{self.pos[1]};{self.ship_type};{self.color}'