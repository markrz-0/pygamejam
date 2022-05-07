import json

import pygame
import numpy as np
import threading
from config import *
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
            img_path=col
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

        self.net_queue = []
        self.selected_ship = 0
        self.ships = [
            'carrier',
            'squadron'
        ]

        self.add(self.gtxt)

        self.stations = []
        self.s = None # socket

    def start(self, session):
        num = session['stations_number']
        self.s = session['client']
        for _ in range(num):
            st = Station((0, 0))
            self.add(st)
            self.stations.append(st)

        threading.Thread(target=self.networking).start()

    def on_mouse_down(self, event: pygame.event.Event):
        pos = event.pos
        world_pos = (pos[0] + self.camera.position[0], pos[1] + self.camera.position[1])
        self.net_queue.append(
            f'{world_pos[0]};{world_pos[1]};{self.selected_ship}'.encode('utf-8')
        ) # X;Y;S

    def on_key_down(self, event: pygame.event.Event):
        if event.key == pygame.K_e:
            self.selected_ship += 1
            if self.selected_ship == len(self.ships):
                self.selected_ship = 0

        if event.key == pygame.K_q:
            self.selected_ship -= 1
            if self.selected_ship == -1:
                self.selected_ship = len(self.ships) - 1


    def post_update(self, g, session: dict): # TODO: maybe remove?
        self.gtxt.text.text = f"Seleted: {self.ships[self.selected_ship]}"

    def process_data(self, data):
        data = json.loads(data.decode('utf-8'))
        # stations
        stations_string = data['stations']
        if stations_string != '':
            stations = stations_string.split('#')
            for i, s in enumerate(stations):
                x, y, c = s.split(';')
                self.stations[i].position = (int(x), int(y))


    def networking(self):
        self.s.send(OK.encode('utf-8'))
        while True: # TODO: infinite loop oops
            data = self.s.recv(BUF_SIZE)
            self.process_data(data)

            msg = OK.encode('utf-8')
            if len(self.net_queue) > 0:
                msg = self.net_queue.pop()

            self.s.send(msg)
