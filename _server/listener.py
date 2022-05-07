import socket
from _server import client
from config import *

class Listener:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((IP, PORT))

    def start(self, on_connect):
        """
        :param on_connect: callback with arg (_server.client.Client)
        :return:
        """
        self.s.listen()
        while True:
            conn, addr = self.s.accept()
            print("Accepted connection from", addr)
            on_connect(client.Client(conn, addr))