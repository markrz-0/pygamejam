import pygame
import threading
from _server.client import Client
from _server import game
from config import *


class Backend:
    def __init__(self):
        # using list as stack
        self.connected = []

        self.clock = pygame.time.Clock()

    def add_connection(self, client: Client) -> None:
        self.connected.append(client)

    def start(self):
        while True:
            self.clock.tick(60)

            if len(self.connected) >= 2:
                cl1 = self.connected.pop()
                cl2 = self.connected.pop()
                g = game.Game()
                threading.Thread(target=g.create, args=(cl1, cl2,)).start()