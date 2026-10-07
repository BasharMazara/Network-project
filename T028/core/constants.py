
MENU_TEXT = """
========================
Network Diagnostic System
========================
1. Ping Host
2. Trace Route
3. DNS Lookup
4. IP Configuration
5. Routing Table
6. ARP Table
7. Active TCP Connections
8. Exit
"""

# Maps menu option -> (command_keyword, requires_host_parameter)
MENU_OPTIONS = {
    "1": ("PING", True),
    "2": ("TRACERT", True),
    "3": ("NSLOOKUP", True),
    "4": ("IPCONFIG", False),
    "5": ("ROUTE", False),
    "6": ("ARP", False),
    "7": ("NETSTAT", False),
    "8": ("EXIT", False),
}

VALID_COMMANDS = {"PING", "TRACERT", "NSLOOKUP", "IPCONFIG", "ROUTE", "ARP", "NETSTAT", "EXIT"}
HOST_REQUIRED_COMMANDS = {"PING", "TRACERT", "NSLOOKUP"}
