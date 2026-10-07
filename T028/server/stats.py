

import json
import threading
import time
from collections import Counter
from pathlib import Path

from core.utils import now_str


class ServerStats:
    def __init__(self, stats_file: str = None):
        self._lock = threading.Lock()
        self.start_time = time.time()
        self.total_commands = 0
        self._active_clients = set()
        self.total_client_connections = 0
        self.last_execution_time = None
        self.command_counter = Counter()
        self.execution_times = []
        self.success_count = 0
        self.failure_count = 0

        self.stats_file = Path(stats_file) if stats_file else None
        if self.stats_file:
            self.stats_file.parent.mkdir(parents=True, exist_ok=True)
        self._persist()  # write an initial (empty) snapshot on startup

    # --- connection tracking -------------------------------------------------
    def register_connection(self, client_addr):
        with self._lock:
            self._active_clients.add(client_addr)
            self.total_client_connections += 1
        self._persist()

    def unregister_connection(self, client_addr):
        with self._lock:
            self._active_clients.discard(client_addr)
        self._persist()

    # --- command tracking ------------------------------------------------------
    def record_command(self, command, execution_time, success):
        with self._lock:
            self.total_commands += 1
            self.command_counter[command] += 1
            self.execution_times.append(execution_time)
            self.last_execution_time = execution_time
            if success:
                self.success_count += 1
            else:
                self.failure_count += 1
        self._persist()

    def get_uptime(self):
        return time.time() - self.start_time

    def snapshot(self):
        with self._lock:
            most_common = self.command_counter.most_common(1)
            avg_exec = (
                sum(self.execution_times) / len(self.execution_times)
                if self.execution_times
                else 0.0
            )
            return {
                "total_commands": self.total_commands,
                "currently_connected_clients": len(self._active_clients),
                "total_client_connections": self.total_client_connections,
                "last_execution_time": self.last_execution_time,
                "uptime_seconds": self.get_uptime(),
                "most_frequent_command": most_common[0][0] if most_common else "N/A",
                "average_execution_time": avg_exec,
                "success_count": self.success_count,
                "failure_count": self.failure_count,
                "command_counter": dict(self.command_counter),
            }

    # --- persistence to data/stats.json -----------------------------------------
    def _persist(self):

        if not self.stats_file:
            return
        try:
            data = self.snapshot()
            data["last_updated"] = now_str()
            with open(self.stats_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            print(f"[!] Warning: could not write stats file {self.stats_file}: {e}")
