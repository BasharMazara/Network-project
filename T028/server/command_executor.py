
import platform
import subprocess

SYSTEM = platform.system()  # e.g. 'Windows', 'Linux', 'Darwin'
COMMAND_TIMEOUT_SECONDS = 30


def _build_command(command: str, params: str):
    if command == "PING":
        return ["ping", "-n", "4", params] if SYSTEM == "Windows" else ["ping", "-c", "4", params]

    if command == "TRACERT":
        if SYSTEM == "Windows":
            return ["tracert", "-h", "15", params]
        return ["traceroute", "-m", "15", params]

    if command == "NSLOOKUP":
        return ["nslookup", params]

    if command == "IPCONFIG":
        if SYSTEM == "Windows":
            return ["ipconfig", "/all"]
        return ["ip", "addr", "show"]

    if command == "ROUTE":
        if SYSTEM == "Windows":
            return ["route", "print"]
        return ["ip", "route", "show"]

    if command == "ARP":
        if SYSTEM == "Windows":
            return ["arp", "-a"]
        return ["arp", "-a"]

    if command == "NETSTAT":
        if SYSTEM == "Windows":
            return ["netstat", "-ano"]
        return ["netstat", "-tunap"]

    return None


def execute_command(command: str, params: str):

    command = command.upper()
    cmd_list = _build_command(command, params)

    if cmd_list is None:
        return False, f"Unsupported command: {command}"

    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
        output = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()
        success = result.returncode == 0
        if not output:
            output = "(command produced no output)"
        return success, output

    except subprocess.TimeoutExpired:
        return False, f"Command timed out after {COMMAND_TIMEOUT_SECONDS} seconds."
    except FileNotFoundError:
        return False, (
            f"The system utility for '{command}' ('{cmd_list[0]}') "
            f"was not found on this {SYSTEM} machine."
        )
    except Exception as e:
        return False, f"Unexpected error while executing {command}: {e}"
