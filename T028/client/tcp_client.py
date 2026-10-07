
import socket

from core.protocol import send_message, recv_message


class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_command(self, command, params=""):
        send_message(self.sock, {"command": command, "params": params})
        return recv_message(self.sock)

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
