import pygame
import numpy as np
import threading
from engine import colors, colliders, helpers, activity, border, text, gameObject


def distance(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

class Station(gameObject.GameObject):
    BLUE = '_client/img/station_blue.png'
    FREE = '_client/img/station_yellow.png'
    RED = '_client/img/station_red.png'

    def __init__(self, pos, col='_client/img/station_yellow.png'):
        super().__init__(
            collider=colliders.Collider.CIRCLE,
            circle_radius=gameObject.CircleRadius.ANGLED,
            position=pos,
            img_path=col,
        )

    def set_color(self, img_path):
        self.img = pygame.image.load(img_path)


class GalaxyText(gameObject.GameObject):
    def __init__(self):
        super().__init__(
            collider=colliders.Collider.RECT,
            position=(20, 20),
            text=text.Text('Galaxy', 'monospace', font_percent_size=0.05),
            x_axis=gameObject.PositionOptions.START,
            y_axis=gameObject.PositionOptions.START,

        )


class GalaxyActivity(activity.BaseActivity):
    def __init__(self, window_size):
        super().__init__(bg_path='_client/img/bg.png', window_size=window_size)

        self.gtxt = GalaxyText()

        self.add(self.gtxt)

    def on_mouse_down(self, event: pygame.event.Event):
        pos = event.pos
        world_pos = (pos[0] + self.camera.position[0], pos[1] + self.camera.position[1])
        # TODO: add to queue ADD SHIP

    def post_update(self, g, session: dict):
        self.gtxt.text.text = f"Cam {self.camera.position}"