
import json
import threading
from pathlib import Path

from core.utils import now_str


class RequestLogger:
    def __init__(self, log_file: str):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        if not self.log_file.exists():
            self.log_file.touch()

    def log(self, client_ip, client_port, command, parameters, execution_time, status):
        entry = {
            "timestamp": now_str(),
            "client_ip": client_ip,
            "client_port": client_port,
            "command": command,
            "parameters": parameters,
            "execution_time": round(execution_time, 4),
            "status": status,
        }
        with self._lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        return entry

    def read_all(self):
        """Read and parse every log entry, oldest first."""
        entries = []
        with self._lock:
            if self.log_file.exists():
                with open(self.log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        return entries

    def raw_bytes(self):
        with self._lock:
            if not self.log_file.exists():
                return b""
            return self.log_file.read_bytes()
