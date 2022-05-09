import time

class Client:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.last_recv = time.time()
        self.elixir = 0