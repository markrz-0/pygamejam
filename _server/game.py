import json
import time
import threading
from _server import client
from _shared.station import Stations
from config import *


class Game:
    def __init__(self):
        self.client1 = None
        self.client2 = None
        self.crash = 0

        self.ships = []
        self.explosions = []
        self.stations = [
            Stations((1000, 1000), Stations.FREE)
        ]

    def stations_string(self):
        strings = [str(s) for s in self.stations]
        return '#'.join(strings)

    def handle_client(self, cl: client.Client):
        cl.conn.send(str(len(self.stations)).encode('utf-8'))
        ok_signal = cl.conn.recv(BUF_SIZE)

        cl.last_recv = time.time()

        if ok_signal.decode('utf-8') != OK:
            print("Client sent response other than OK:", ok_signal.decode('utf-8'))
            self.crash += 1
            return

        while True:
            time.sleep(0.016) # around 60 per second
            data = {
                "stations": self.stations_string() # TODO: add other data
            }
            data = json.dumps(data).encode('utf-8')
            cl.conn.send(data)


            data = cl.conn.recv(BUF_SIZE)
            data = data.decode('utf-8')
            if data == OK:
                pass
            else:
                pass # TODO: process add ship

    def create(self, client1: client.Client, client2: client.Client):
        self.client1 = client1
        self.client2 = client2


        threading.Thread(target=self.handle_client, args=(self.client1,)).start()
        threading.Thread(target=self.handle_client, args=(self.client2,)).start()

        # TODO: client connection failures
        # while True:
        #     time.sleep(0.016)
        #     t = time.time()
        #     if t - self.client1.last_recv > DISCONNECT_THRESHOLD:
        #         psas

