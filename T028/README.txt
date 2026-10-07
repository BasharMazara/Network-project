================================================================
 ENCS3320 - Computer Networks (Term 1253)
 Project 1 - Socket Programming
 Team: T028
================================================================

TEAM MEMBERS
------------
Name    : Bashar Mazara
ID      : 1211772
Section : 1


PROJECT OVERVIEW
-----------------
This project implements a Network Diagnostic System made of three
communicating components, all built using ONLY Python's standard
library (socket, threading, os, subprocess, time, datetime, json,
pathlib):

  1. A multi-threaded TCP Server that executes network diagnostic
     commands (Ping, Traceroute, DNS Lookup, IP Configuration,
     Routing Table, ARP Table, Active TCP Connections) on its host
     machine and returns the results to clients.
  2. A TCP Client with an interactive text menu for sending those
     requests.
  3. An HTTP Web Server (built from raw sockets) that exposes a
     Home, Dashboard, Command History, Statistics, Search, and
     Download page over a separate port.

Both the TCP server and the HTTP server run in the SAME process
(run_server.py) and share the same request log and live statistics,
so the web interface always reflects what the TCP server is doing.


PORT NUMBERS (derived from student ID 1211772, per the assignment's
Part D rule: last three digits of a team member's ID + 5000 / 6000)
-----------------------------------------------------------------
  TCP Diagnostic Server Port : 5772   (772 + 5000)
  HTTP Web Server Port       : 6772   (772 + 6000)

Both ports (and every other configurable parameter) live in
config.json and can be changed there without touching any code.


FOLDER STRUCTURE
-----------------
  T028/
  |-- README.txt            <- this file
  |-- run_server.py          <- entry point: starts TCP + HTTP servers
  |-- run_client.py          <- entry point: starts the interactive client
  |-- config.json             <- all configurable parameters
  |-- config/                <- config loading module
  |-- core/                  <- shared protocol, constants, validation, utils
  |-- server/                <- TCP server, per-client threads, command
  |                             execution, logging, statistics
  |-- client/                <- TCP client, interactive menu, response display
  |-- web/                   <- HTTP server, routing, HTML page generation
  |-- logs/                  <- server.log is created here at runtime
  |-- data/                  <- reserved for runtime/statistics data
  |-- screenshots/            <- put demonstration screenshots here


REQUIREMENTS
-------------
  - Python 3.8+ (no external/third-party packages required)
  - On Linux, the following OS utilities should be installed for full
    command coverage: iputils-ping, traceroute, dnsutils (nslookup),
    iproute2 (ip), net-tools (arp, netstat, route)
      e.g. on Debian/Ubuntu:
        sudo apt install iputils-ping traceroute dnsutils iproute2 net-tools
  - On Windows, ping/tracert/nslookup/ipconfig/route/arp/netstat are
    already built in - no extra installation is needed.


HOW TO CONFIGURE
------------------
Open config.json and adjust as needed:
  {
    "tcp_host"            : interface the TCP server binds to (0.0.0.0 = all)
    "tcp_port"             : 5772
    "http_host"            : interface the HTTP server binds to
    "http_port"             : 6772
    "log_file"              : path to the request log file
    "stats_file"            : reserved path for persisted statistics
    "max_clients"           : max pending TCP connections in the listen backlog
    "client_connect_host"   : host the CLIENT connects to (127.0.0.1 for
                               same-machine testing, or the server's IP
                               address for testing across two machines)
    "students"              : team roster shown on the web Home page
    "course_description"    : text shown on the web Home page
  }


HOW TO RUN
------------
1) Start the server (starts both the TCP server and the HTTP server):

     python3 run_server.py

   You should see confirmation that both servers are listening, e.g.:
     TCP diagnostic server : 0.0.0.0:5772
     HTTP web interface    : http://0.0.0.0:6772/home

2) In one or more separate terminals, start a client:

     python3 run_client.py

   Follow the on-screen menu (1-8) to send diagnostic commands. You
   can run several clients at the same time to demonstrate the
   multi-threaded server handling concurrent connections.

3) Open the web interface in a browser:

     http://127.0.0.1:6772/home

   Then browse the Dashboard, Command History, Statistics, Search,
   and Download tabs. Try an unknown URL (e.g. /doesnotexist) to see
   the custom 404 page.


TESTING ACROSS TWO MACHINES
------------------------------
On the SERVER machine: run `python3 run_server.py` (tcp_host/http_host
left as 0.0.0.0 so it accepts connections from any interface).

On the CLIENT machine: edit config.json's "client_connect_host" to the
server machine's IP address, then run `python3 run_client.py`. Make
sure the server machine's firewall allows inbound connections on
ports 5772 and 6772.


DEMONSTRATING HTTP STATUS CODES
-----------------------------------
  200 OK          -> any valid tab, e.g. /home, /dashboard
  404 Not Found   -> request an undefined page, e.g. /nosuchpage
  403 Forbidden   -> request an internal path, e.g. /data or /config
  400 Bad Request -> send a malformed HTTP request (e.g. via
                     `printf 'GET\r\n\r\n' | nc 127.0.0.1 6772`)



