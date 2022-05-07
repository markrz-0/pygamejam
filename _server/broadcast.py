import socket
import time
from config import *

class Broadcast:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('', 0))
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.data = (BROADCAST + IP).encode('utf-8')

    def start(self, interval=5):
        while True:
            self.s.sendto(self.data, ('<broadcast>', PORT))
            time.sleep(interval)
