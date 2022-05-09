import json
import time
import threading
import pygame
from _server import client
from _shared.station import Station
from _shared.ship import Ship
from config import *


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
        cl.conn.send((str(len(self.stations)) + ';' + str(index)).encode('utf-8'))
        ok_signal = cl.conn.recv(BUF_SIZE)

        cl.last_recv = time.time()

        if ok_signal.decode('utf-8') != OK:
            print("Client sent response other than OK:", ok_signal.decode('utf-8'))
            self.crash += 1
            return

        while True:
            time.sleep(0.016) # around 60 per second
            data = {
                "stations": self.stations_string(),
                'ships': self.ships_string() # TODO: add other data
            }
            data = json.dumps(data).encode('utf-8')
            cl.conn.send(data)


            data = cl.conn.recv(BUF_SIZE)
            data = data.decode('utf-8')
            if data != OK: # meaning client sent some data (ship placement)
                print("client", index, '-', data)
                x, y, s = [int(x) for x in data.split(';')]
                self.ships.append(Ship((x, y), s, index))

    def create(self, client1: client.Client, client2: client.Client):
        self.client1 = client1
        self.client2 = client2


        threading.Thread(target=self.handle_client, args=(self.client1, 1)).start()
        threading.Thread(target=self.handle_client, args=(self.client2, 2)).start()

        # TODO: client connection failures & ship movemnet and firing
        while True:
            delta = self.clock.tick(60)

            t = time.time()
            if t - self.client1.last_recv > DISCONNECT_THRESHOLD:
                self.winner = 2
            elif t - self.client2.last_recv > DISCONNECT_THRESHOLD:
                self.winner = 1

            for s in self.ships:
                if s.color == 1: # blue
                    s.pos = (s.pos[0], s.pos[1] - delta * s.speed)
                elif s.color == 2: # red
                    s.pos = (s.pos[0], s.pos[1] + delta * s.speed)


