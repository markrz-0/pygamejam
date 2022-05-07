class Border:
    def __init__(self, color: tuple[int, int, int], thickness: int, radius=-1, padding=0):
        self.color = color
        self.thickness = thickness
        self.radius = radius
        self.padding = padding