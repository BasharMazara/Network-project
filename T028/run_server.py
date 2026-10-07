#!/usr/bin/env python3

import time

from config.config_manager import ConfigManager
from server.tcp_server import TCPServer
from web.http_server import HTTPServer


def main():
    config = ConfigManager("config.json")

    tcp_server = TCPServer(
        host=config.get("tcp_host", "0.0.0.0"),
        port=config.get("tcp_port"),
        log_file=config.get("log_file", "logs/server.log"),
        max_clients=config.get("max_clients", 10),
        stats_file=config.get("stats_file", "data/stats.json"),
    )

    http_server = HTTPServer(
        host=config.get("http_host", "0.0.0.0"),
        port=config.get("http_port"),
        config=config,
        logger=tcp_server.logger,   # shared logger
        stats=tcp_server.stats,     # shared stats
    )

    print("=" * 60)
    print(" ENCS3320 - Network Diagnostic System - Server")
    print(f" Team: {config.get('team_number')}")
    print("=" * 60)

    tcp_server.start_in_background()
    http_server.start_in_background()

    print(f"\nTCP diagnostic server : {config.get('tcp_host')}:{config.get('tcp_port')}")
    print(f"HTTP web interface     : http://{config.get('http_host')}:{config.get('http_port')}/home")
    print("\nPress Ctrl+C to stop the server.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Main] Server stopped.")


if __name__ == "__main__":
    main()
