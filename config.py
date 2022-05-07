import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 6969

BUF_SIZE = 2048

DISCONNECT_THRESHOLD = 3.5 # in seconds

STATION_HEALTH = 1000

BROADCAST = "z9cGhzfo"

OK = 'OK'
READY = 'RD'
DISCONNECT = 'DC'
