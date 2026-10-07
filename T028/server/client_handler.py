
import time

from core.protocol import send_message, recv_message
from core.validation import validate_request
from core.utils import now_str
from server.command_executor import execute_command


def handle_client(conn, addr, logger, stats):
    client_ip, client_port = addr
    stats.register_connection(addr)
    print(f"[+] Client connected: {client_ip}:{client_port}")

    try:
        while True:
            msg = recv_message(conn)
            if msg is None:
                break  # client disconnected

            command = str(msg.get("command", "")).strip().upper()
            params = str(msg.get("params", "")).strip()

            if command == "EXIT":
                send_message(conn, {
                    "status": "success",
                    "output": "Goodbye.",
                    "execution_time": 0,
                    "timestamp": now_str(),
                })
                break

            valid, error = validate_request(command, params)
            if not valid:
                send_message(conn, {
                    "status": "error",
                    "output": error,
                    "execution_time": 0,
                    "timestamp": now_str(),
                })
                logger.log(client_ip, client_port, command, params, 0, "Failure")
                stats.record_command(command or "UNKNOWN", 0, False)
                continue

            start = time.time()
            success, output = execute_command(command, params)
            exec_time = time.time() - start

            send_message(conn, {
                "status": "success" if success else "error",
                "output": output,
                "execution_time": round(exec_time, 4),
                "timestamp": now_str(),
            })

            logger.log(
                client_ip, client_port, command, params,
                exec_time, "Success" if success else "Failure",
            )
            stats.record_command(command, exec_time, success)

    except (ConnectionResetError, BrokenPipeError):
        pass
    except Exception as e:
        print(f"[!] Error handling client {addr}: {e}")
    finally:
        stats.unregister_connection(addr)
        conn.close()
        print(f"[-] Client disconnected: {client_ip}:{client_port}")
