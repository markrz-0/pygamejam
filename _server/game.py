import json
import time
import threading

import black as black
import pygame
import numpy as np

import config
from _server import client
from _shared.station import Station
from _shared.ship import Ship
from config import *

def distance(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

class Game:
    def __init__(self):
        self.client1 = None
        self.client2 = None
        self.crash = 0

        self.winner = 0

        self.ships = []
        self.explosions = []
        self.stations = [
            Station((100, 100), Station.RED),
            Station((1000, 100), Station.RED),
            Station((1900, 100), Station.RED),
            Station((700, 300), Station.RED),
            Station((1300, 300), Station.RED),

            Station((300, 1000), Station.FREE),
            Station((1000, 1000), Station.FREE),
            Station((1700, 1000), Station.FREE),

            Station((100, 1900), Station.BLUE),
            Station((1000, 1900), Station.BLUE),
            Station((1900, 1900), Station.BLUE),
            Station((700, 1700), Station.BLUE),
            Station((1300, 1700), Station.BLUE),
        ]

        self.clock = pygame.time.Clock()

    def stations_string(self):
        strings = [str(s) for s in self.stations]
        return '#'.join(strings)

    def ships_string(self):
        strings = [str(s) for s in self.ships]
        return '#'.join(strings)

    def handle_client(self, cl: client.Client, index):
        clock = pygame.time.Clock()

        cl.conn.send((str(len(self.stations)) + ';' + str(index)).encode('utf-8'))
        ok_signal = cl.conn.recv(BUF_SIZE)

        cl.last_recv = time.time()

        if ok_signal.decode('utf-8') != OK:
            print("Client sent response other than OK:", ok_signal.decode('utf-8'))
            self.crash += 1
            return

        run = True

        while run:
            delta = clock.tick(60) # delta is in ms
            cl.elixir += delta * 0.001 * config.ELIXIR_PER_SECOND
            data = {
                "stations": self.stations_string(),
                'ships': self.ships_string(),
                'winner': self.winner, # TODO: explosions
                'elixir': int(cl.elixir)
            }

            data = json.dumps(data).encode('utf-8')
            cl.conn.send(data)

            if self.winner:
                run = False

            data = cl.conn.recv(BUF_SIZE)
            cl.last_recv = time.time()
            data = data.decode('utf-8')
            if data != OK: # meaning client sent some data (ship placement)
                # TODO: elixir
                print("client", index, '-', data)
                x, y, s = [int(x) for x in data.split(';')]



                can = False
                if config.ELIXIR_FOR_SHIP[s] < cl.elixir:
                    for st in self.stations:
                        if st.color == index and distance(st.pos, (x, y)) < 300:
                            can = True
                            break

                if can:
                    cl.elixir -= config.ELIXIR_FOR_SHIP[s]
                    self.ships.append(Ship((x, y), s, index))

        cl.conn.close()

    def create(self, client1: client.Client, client2: client.Client):
        self.client1 = client1
        self.client2 = client2


        threading.Thread(target=self.handle_client, args=(self.client1, 1)).start()
        threading.Thread(target=self.handle_client, args=(self.client2, 2)).start()

        # TODO: ships turning
        self.client1.last_recv = time.time()
        self.client2.last_recv = time.time()

        while True:
            delta = self.clock.tick(60)

            t = time.time()
            if t - self.client1.last_recv > DISCONNECT_THRESHOLD:
                print("W#1")
                self.winner = 2
                self.client1.conn.close()
                break
            elif t - self.client2.last_recv > DISCONNECT_THRESHOLD:
                print("W#2")
                self.winner = 1
                self.client2.conn.close()
                break

            for i, s in enumerate(self.ships):
                move = True
                nearest = None
                nearest_d = 3000
                for st in self.stations:
                    if s.color != st.color:
                        print(s.color, st.color)
                        d = distance(s.pos, st.pos)
                        if d < s.range:
                            move = False
                            if d < nearest_d:
                                nearest = st
                                nearest_d = d

                for s2 in self.ships:
                    if s.color != s2.color:
                        d = distance(s.pos, s2.pos)
                        if d < s.range:
                            move = False
                            if d < nearest_d:
                                nearest = s2
                                nearest_d = d

                s.reload(delta)

                if nearest is not None:
                    if s.reloaded:
                        s.shoot() # TODO: explosions
                        nearest.health -= s.dmg
                        nearest.last_hit = s.color

                if move:
                    if s.color == 1: # blue
                        s.pos = (s.pos[0], s.pos[1] - delta * s.speed)
                    elif s.color == 2: # red
                        s.pos = (s.pos[0], s.pos[1] + delta * s.speed)

                if s.health < 0 or abs(s.pos[0] - 1000) > 1400 or abs(s.pos[1] - 1000) > 1400:
                    del self.ships[i]

            blue = 0
            red = 0
            for i, st in enumerate(self.stations):
                if st.health < 0:
                    self.stations[i].health = config.STATION_HEALTH
                    self.stations[i].color = self.stations[i].last_hit

                if st.color == 1:
                    blue += 1
                elif st.color == 2:
                    red += 1

                st.target = None
                nearest_d = 3000
                for s in self.ships:
                    if s.color != st.color:
                        d = distance(st.pos, s.pos)
                        if d < config.STATION_RANGE and d < STATION_RANGE:
                            if d < nearest_d:
                                st.target = s
                                nearest_d = d

                st.reload(delta)

                if st.reloaded and st.target is not None:
                    st.shoot() # station has target
                    # TODO: explosions

            if blue == 0:
                print("W#3")
                self.winner = 2
                break
            elif red == 0:
                print("W#4")
                self.winner = 1
                break

            self.client1.elixir += delta * 0.001 * blue * config.ELIXIR_PER_STATION
            self.client2.elixir += delta * 0.001 * red * config.ELIXIR_PER_STATION