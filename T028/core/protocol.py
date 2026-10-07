
import json
import struct

HEADER_SIZE = 4  # bytes, unsigned int, network byte order


def send_message(sock, data: dict):
    payload = json.dumps(data).encode("utf-8")
    header = struct.pack("!I", len(payload))
    sock.sendall(header + payload)


def _recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def recv_message(sock):
    header = _recv_exact(sock, HEADER_SIZE)
    if header is None:
        return None
    (length,) = struct.unpack("!I", header)
    payload = _recv_exact(sock, length)
    if payload is None:
        return None
    try:
        return json.loads(payload.decode("utf-8"))
    except json.JSONDecodeError:
        return None
