
def print_response(response: dict):
    if response is None:
        print("\n[!] No response received from server (connection may have closed).\n")
        return

    status = response.get("status", "unknown").upper()
    output = response.get("output", "")
    exec_time = response.get("execution_time", 0)
    timestamp = response.get("timestamp", "")

    print("\n" + "-" * 60)
    print(f" Status         : {status}")
    print(f" Timestamp      : {timestamp}")
    print(f" Execution Time : {exec_time}s")
    print("-" * 60)
    print(output)
    print("-" * 60 + "\n")
