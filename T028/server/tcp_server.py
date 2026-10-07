

import socket
import threading

from server.client_handler import handle_client
from server.logger import RequestLogger
from server.stats import ServerStats


class TCPServer:
    def __init__(self, host, port, log_file, max_clients=10, stats_file=None):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.logger = RequestLogger(log_file)
        self.stats = ServerStats(stats_file=stats_file)
        self._sock = None

    def start(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        self._sock.listen(self.max_clients)
        print(f"[TCP Server] Listening on {self.host}:{self.port}")

        try:
            while True:
                conn, addr = self._sock.accept()
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(conn, addr, self.logger, self.stats),
                    daemon=True,
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("\n[TCP Server] Shutting down.")
        finally:
            if self._sock:
                self._sock.close()

    def start_in_background(self):

        t = threading.Thread(target=self.start, daemon=True)
        t.start()
        return t
