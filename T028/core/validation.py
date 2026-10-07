

import re

from core.constants import VALID_COMMANDS, HOST_REQUIRED_COMMANDS

# Only allow characters that are legal in hostnames / IPv4 / IPv6 addresses.
HOSTNAME_PATTERN = re.compile(r"^[a-zA-Z0-9.\-:]+$")
MAX_HOSTNAME_LENGTH = 253


def validate_request(command: str, params: str):

    if not command:
        return False, "No command was provided."

    if command not in VALID_COMMANDS:
        return False, f"Invalid command: '{command}'."

    if command in HOST_REQUIRED_COMMANDS:
        if not params:
            return False, f"{command} requires a hostname or IP address parameter."
        if len(params) > MAX_HOSTNAME_LENGTH:
            return False, "Hostname/IP parameter is too long."
        if not HOSTNAME_PATTERN.match(params):
            return False, "Invalid hostname/IP format. Only letters, digits, '.', '-' and ':' are allowed."

    return True, None
