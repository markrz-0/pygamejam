import pygame
import json
import threading
from config import *
from engine import colors, helpers, activity

CHANGE = 500

class LoadingActivity(activity.BaseActivity):
    def __init__(self, window_size):
        super().__init__(bg_path='_client/img/bg.png', window_size=window_size)
        self.next_change = CHANGE
        self.dots = 0
        self.make_dots = True

        self.ds = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ds.bind(('', PORT))
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.display_text = ''

    def start(self, session):
        self.display_text = 'Loading'
        self.make_dots = True

        self.ds = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ds.bind(('', PORT))
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread(target=self.connect).start()

    def connect(self):
        while True:
            data = self.ds.recv(BUF_SIZE)
            data = data.decode('utf-8')
            if data.startswith(BROADCAST):
                ip = data[len(BROADCAST):]
                helpers.add_session_data('server_ip', ip)
                self.ds.close()

                self.s.connect((ip, PORT))
                helpers.add_session_data('client', self.s)

                self.display_text = 'Waiting for server'

                threading.Thread(target=self.waiting_for_server).start()
                return

    def waiting_for_server(self):
        while True:
            data = self.s.recv(BUF_SIZE) # waiting for READY signal from server
            helpers.add_session_data('stations_number', int(data.decode('utf-8')))
            helpers.change_activity('galaxy')
            return

    def update(self, g, session):
        super().update(g, session)
        w, h = g.window.get_size()
        font = pygame.font.SysFont('monospace', h // 10)

        other = ''
        if self.make_dots:
            other = "." * self.dots

        text = font.render(self.display_text + other, True, colors.WHITE)
        tw, th = text.get_size()
        g.window.blit(text, ((w - tw)//2, (h - th)//2))

        self.next_change -= g.deltatime

        if self.next_change < 0:
            self.dots += 1
            if self.dots > 3:
                self.dots = 0
            self.next_change = CHANGE
