import json
import time
import threading
from _server import client
from config import *


class Game:
    def __init__(self):
        self.client1 = None
        self.client2 = None
        self.crash = 0

        # self.client1_queue = []
        # self.client2_queue = []

        self.ships = []
        self.explosions = []
        self.stations = [

        ]

    def handle_client(self, cl: client.Client, client_queue: list):
        cl.conn.send(str().encode('utf-8'))
        ok_signal = cl.conn.recv(BUF_SIZE)

        cl.last_recv = time.time()

        if ok_signal.decode('utf-8') != OK:
            print("Client sent response other than OK:", ok_signal.decode('utf-8'))
            self.crash += 1
            return

        while True:
            time.sleep(0.016) # around 60 per second
            if len(client_queue) > 0:
                data = {
                    'map': self.map.to_dict() # TODO: remove
                }

                data = json.dumps(data).encode('utf-8')

                cl.conn.send(data)

                data, addr = cl.conn.recv(BUF_SIZE)
                cl.last_recv = time.time()

                decoded_data = data.decode('utf-8')
                # TODO: ships

    def create(self, client1: client.Client, client2: client.Client):
        self.client1 = client1
        self.client2 = client2


        threading.Thread(target=self.handle_client, args=(self.client1, self.client1_queue)).start()
        threading.Thread(target=self.handle_client, args=(self.client2, self.client2_queue)).start()

        # TODO: client connection failures
        # while True:
        #     time.sleep(0.016)
        #     t = time.time()
        #     if t - self.client1.last_recv > DISCONNECT_THRESHOLD:
        #         psas

