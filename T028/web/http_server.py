"""
http_server.py
---------------
A simple HTTP web server implemented directly with sockets (no http.server,
no external frameworks - per the assignment's "standard socket library
only" rule). Listens on its own port (separate from the TCP diagnostic
server) and serves the web interface tabs via web/router.py.

Each incoming connection is handled in its own thread so a slow client
cannot block the rest of the web interface.
"""

import socket
import threading

from web.router import route_request
from web.http_utils import build_response
from web import pages


class HTTPServer:
    def __init__(self, host, port, config, logger, stats):
        self.host = host
        self.port = port
        self.config = config
        self.logger = logger
        self.stats = stats
        self._sock = None

    def start(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        self._sock.listen(20)
        print(f"[HTTP Server] Listening on {self.host}:{self.port}")

        try:
            while True:
                conn, addr = self._sock.accept()
                t = threading.Thread(target=self._handle, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\n[HTTP Server] Shutting down.")
        finally:
            if self._sock:
                self._sock.close()

    def start_in_background(self):
        t = threading.Thread(target=self.start, daemon=True)
        t.start()
        return t

    def _handle(self, conn, addr):
        try:
            conn.settimeout(5)
            data = b""
            while b"\r\n\r\n" not in data:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk

            if not data:
                conn.close()
                return

            request_text = data.decode("utf-8", errors="replace")
            response = route_request(request_text, self.config, self.logger, self.stats)
            conn.sendall(response)

        except socket.timeout:
            try:
                conn.sendall(build_response(400, pages.error_page(400, "Request timed out.")))
            except OSError:
                pass
        except Exception as e:
            try:
                conn.sendall(build_response(500, f"<h1>500 Internal Server Error</h1><p>{e}</p>"))
            except OSError:
                pass
        finally:
            conn.close()
