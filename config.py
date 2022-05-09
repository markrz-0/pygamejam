import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 6969

BUF_SIZE = 8192

DISCONNECT_THRESHOLD = 3.5 # in seconds

STATION_HEALTH = 1000
STATION_RANGE = 200
STATION_DMG = 3
STATION_COOLDOWN = 1000 # in ms

ELIXIR_PER_SECOND = 1
ELIXIR_PER_STATION = 0.1

ELIXIR_FOR_SHIP = [
    None,
    2
]

BROADCAST = "z9cGhzfo"

OK = 'OK'
READY = 'RD'
DISCONNECT = 'DC'
