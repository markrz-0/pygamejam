import threading
from _server import broadcast, listener, backend

class Server:
    def __init__(self):
        self.broadcast = broadcast.Broadcast()
        self.listener = listener.Listener()
        self.backend = backend.Backend()

    def run(self):
        threading.Thread(target=self.broadcast.start).start()

        threading.Thread(target=self.listener.start,
                         args=(self.backend.add_connection,)).start()

        threading.Thread(target=self.backend.start).start()


if __name__ == '__main__':
    server = Server()
    server.run()