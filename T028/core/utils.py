

from datetime import datetime


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_seconds(seconds: float, decimals: int = 4) -> str:
    return f"{seconds:.{decimals}f}s"


def format_uptime(seconds: float) -> str:
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours}h {minutes}m {secs}s"
