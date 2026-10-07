#!/usr/bin/env python3


from config.config_manager import ConfigManager
from client.tcp_client import TCPClient
from client.menu import show_menu, get_selection
from client.display import print_response


def main():
    config = ConfigManager("config.json")
    host = config.get("client_connect_host", "127.0.0.1")
    port = config.get("tcp_port")

    client = TCPClient(host, port)

    try:
        client.connect()
        print(f"Connected to Network Diagnostic Server at {host}:{port}\n")
    except (ConnectionRefusedError, OSError) as e:
        print(f"[!] Could not connect to server at {host}:{port} -> {e}")
        return

    try:
        while True:
            show_menu()
            command, params = get_selection()

            if command is None:
                continue

            if command == "EXIT":
                response = client.send_command("EXIT")
                print_response(response)
                break

            response = client.send_command(command, params)
            print_response(response)

    except KeyboardInterrupt:
        print("\n[Client] Interrupted by user.")
    finally:
        client.close()
        print("[Client] Connection closed.")


if __name__ == "__main__":
    main()
