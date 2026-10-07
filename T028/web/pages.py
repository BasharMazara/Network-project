"""
pages.py
--------
Generates the HTML for every tab of the web interface (Home, Dashboard,
Command History, Statistics, Search) plus the custom error pages. All
pages share a common layout/navigation bar defined in `_layout`.
"""

from html import escape

from core.utils import format_uptime

NAV_ITEMS = [
    ("/home", "Home"),
    ("/dashboard", "Dashboard"),
    ("/history", "Command History"),
    ("/statistics", "Statistics"),
    ("/search", "Search"),
    ("/download", "Download Log"),
]

BASE_CSS = """
    :root {
        --bg: #0f172a;
        --panel: #ffffff;
        --accent: #2563eb;
        --accent-dark: #1e40af;
        --text: #1e293b;
        --muted: #64748b;
        --ok: #16a34a;
        --fail: #dc2626;
        --border: #e2e8f0;
    }
    * { box-sizing: border-box; }
    body {
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
        background: #f1f5f9;
        color: var(--text);
    }
    header {
        background: linear-gradient(135deg, var(--bg), var(--accent-dark));
        color: #fff;
        padding: 22px 32px;
    }
    header h1 { margin: 0; font-size: 22px; }
    header p { margin: 4px 0 0; color: #cbd5e1; font-size: 13px; }
    nav {
        background: var(--panel);
        border-bottom: 1px solid var(--border);
        display: flex;
        gap: 4px;
        padding: 0 24px;
        flex-wrap: wrap;
    }
    nav a {
        text-decoration: none;
        color: var(--muted);
        padding: 14px 16px;
        font-size: 14px;
        font-weight: 600;
        border-bottom: 3px solid transparent;
    }
    nav a.active, nav a:hover {
        color: var(--accent-dark);
        border-bottom: 3px solid var(--accent);
    }
    main { padding: 28px 32px; max-width: 1080px; margin: 0 auto; }
    .card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 22px 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .card h2 { margin-top: 0; font-size: 17px; color: var(--accent-dark); }
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
    }
    .stat-box {
        background: #f8fafc;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .stat-box .value { font-size: 26px; font-weight: 700; color: var(--accent-dark); }
    .stat-box .label { font-size: 12px; color: var(--muted); margin-top: 4px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border); }
    th { background: #f8fafc; color: var(--muted); font-size: 12px; text-transform: uppercase; }
    tr:hover { background: #f8fafc; }
    .badge { padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 700; }
    .badge.success { background: #dcfce7; color: var(--ok); }
    .badge.failure { background: #fee2e2; color: var(--fail); }
    form.search-form { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 6px; }
    form.search-form input {
        padding: 9px 12px; border: 1px solid var(--border); border-radius: 6px; font-size: 13px;
        flex: 1; min-width: 160px;
    }
    form.search-form button {
        padding: 9px 18px; background: var(--accent); color: #fff; border: none;
        border-radius: 6px; font-weight: 600; cursor: pointer;
    }
    form.search-form button:hover { background: var(--accent-dark); }
    .empty { color: var(--muted); font-style: italic; padding: 12px 0; }
    .download-btn {
        display: inline-block; background: var(--accent); color: #fff; text-decoration: none;
        padding: 10px 20px; border-radius: 6px; font-weight: 600;
    }
    .download-btn:hover { background: var(--accent-dark); }
    footer { text-align: center; color: var(--muted); font-size: 12px; padding: 24px; }
    .error-code { font-size: 64px; font-weight: 800; color: var(--accent-dark); margin: 0; }
"""


def _layout(title, active_path, content_html):
    nav_links = ""
    for path, label in NAV_ITEMS:
        cls = "active" if path == active_path else ""
        nav_links += f'<a class="{cls}" href="{path}">{escape(label)}</a>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{escape(title)} - ENCS3320 Network Diagnostic System</title>
    <style>{BASE_CSS}</style>
</head>
<body>
    <header>
        <h1>Network Diagnostic System</h1>
        <p>ENCS3320 - Computer Networks &middot; Project 1 &middot; Team T028</p>
    </header>
    <nav>{nav_links}</nav>
    <main>{content_html}</main>
    <footer>Birzeit University &middot; Faculty of Engineering and Technology &middot; ENCS3320 (Term 1253)</footer>
</body>
</html>"""


# ---------------------------------------------------------------- Home page
def home_page(config):
    students = config.get("students", [])
    rows = "".join(
        f"<tr><td>{escape(s.get('name',''))}</td>"
        f"<td>{escape(str(s.get('student_id','')))}</td>"
        f"<td>{escape(str(s.get('section','')))}</td></tr>"
        for s in students
    )
    content = f"""
    <div class="card">
        <h2>Team Information</h2>
        <p><strong>Team Number:</strong> {escape(config.get('team_number',''))}</p>
        <table>
            <tr><th>Student Name</th><th>Student ID</th><th>Section</th></tr>
            {rows}
        </table>
    </div>
    <div class="card">
        <h2>About This Course</h2>
        <p>{escape(config.get('course_description',''))}</p>
    </div>
    <div class="card">
        <h2>About This Project</h2>
        <p>This system implements a multi-threaded TCP server that executes network
        diagnostic commands (Ping, Traceroute, DNS Lookup, IP Configuration, Routing
        Table, ARP Table, and Active TCP Connections) on behalf of remote TCP clients,
        logs every request, and exposes the collected data through this HTTP web
        interface - built entirely with Python's standard socket library.</p>
    </div>
    """
    return _layout("Home", "/home", content)


# ----------------------------------------------------------- Dashboard page
def dashboard_page(stats):
    s = stats.snapshot()
    last_exec = f"{s['last_execution_time']:.4f}s" if s["last_execution_time"] is not None else "N/A"
    content = f"""
    <div class="card">
        <h2>Live Dashboard</h2>
        <div class="stat-grid">
            <div class="stat-box"><div class="value">{s['total_commands']}</div><div class="label">Commands Executed</div></div>
            <div class="stat-box"><div class="value">{s['currently_connected_clients']}</div><div class="label">Connected Clients (now)</div></div>
            <div class="stat-box"><div class="value">{s['total_client_connections']}</div><div class="label">Total Client Connections</div></div>
            <div class="stat-box"><div class="value">{last_exec}</div><div class="label">Last Execution Time</div></div>
            <div class="stat-box"><div class="value">{format_uptime(s['uptime_seconds'])}</div><div class="label">Server Uptime</div></div>
        </div>
    </div>
    """
    return _layout("Dashboard", "/dashboard", content)


# ------------------------------------------------------- Command History page
def history_page(entries):
    if not entries:
        rows_html = '<tr><td colspan="6" class="empty">No commands have been executed yet.</td></tr>'
    else:
        rows_html = ""
        for e in reversed(entries):
            badge_cls = "success" if e.get("status") == "Success" else "failure"
            rows_html += (
                f"<tr><td>{escape(str(e.get('timestamp','')))}</td>"
                f"<td>{escape(str(e.get('client_ip','')))}</td>"
                f"<td>{escape(str(e.get('command','')))}</td>"
                f"<td>{escape(str(e.get('parameters','')) or '-')}</td>"
                f"<td>{e.get('execution_time','')}s</td>"
                f'<td><span class="badge {badge_cls}">{escape(str(e.get("status","")))}</span></td></tr>'
            )
    content = f"""
    <div class="card">
        <h2>Command History</h2>
        <table>
            <tr><th>Time</th><th>Client IP</th><th>Command</th><th>Parameter</th><th>Execution Time</th><th>Status</th></tr>
            {rows_html}
        </table>
    </div>
    """
    return _layout("Command History", "/history", content)


# --------------------------------------------------------- Statistics page
def statistics_page(stats):
    s = stats.snapshot()
    counter_rows = "".join(
        f"<tr><td>{escape(cmd)}</td><td>{count}</td></tr>"
        for cmd, count in sorted(s["command_counter"].items(), key=lambda x: -x[1])
    ) or '<tr><td colspan="2" class="empty">No data yet.</td></tr>'

    content = f"""
    <div class="card">
        <h2>Overall Statistics</h2>
        <div class="stat-grid">
            <div class="stat-box"><div class="value">{escape(s['most_frequent_command'])}</div><div class="label">Most Frequent Command</div></div>
            <div class="stat-box"><div class="value">{s['average_execution_time']:.4f}s</div><div class="label">Average Execution Time</div></div>
            <div class="stat-box"><div class="value">{s['success_count']}</div><div class="label">Successful Requests</div></div>
            <div class="stat-box"><div class="value">{s['failure_count']}</div><div class="label">Failed Requests</div></div>
        </div>
    </div>
    <div class="card">
        <h2>Command Frequency Breakdown</h2>
        <table>
            <tr><th>Command</th><th>Times Executed</th></tr>
            {counter_rows}
        </table>
    </div>
    """
    return _layout("Statistics", "/statistics", content)


# ------------------------------------------------------------- Search page
def search_page(entries, query):
    command_q = (query.get("command", [""])[0] or "").strip().upper()
    hostname_q = (query.get("hostname", [""])[0] or "").strip().lower()
    ip_q = (query.get("client_ip", [""])[0] or "").strip()

    has_query = bool(command_q or hostname_q or ip_q)
    results = []
    if has_query:
        for e in entries:
            if command_q and command_q not in str(e.get("command", "")).upper():
                continue
            if hostname_q and hostname_q not in str(e.get("parameters", "")).lower():
                continue
            if ip_q and ip_q not in str(e.get("client_ip", "")):
                continue
            results.append(e)

    if not has_query:
        rows_html = '<tr><td colspan="6" class="empty">Enter at least one filter above and click Search.</td></tr>'
    elif not results:
        rows_html = '<tr><td colspan="6" class="empty">No matching commands found.</td></tr>'
    else:
        rows_html = ""
        for e in reversed(results):
            badge_cls = "success" if e.get("status") == "Success" else "failure"
            rows_html += (
                f"<tr><td>{escape(str(e.get('timestamp','')))}</td>"
                f"<td>{escape(str(e.get('client_ip','')))}</td>"
                f"<td>{escape(str(e.get('command','')))}</td>"
                f"<td>{escape(str(e.get('parameters','')) or '-')}</td>"
                f"<td>{e.get('execution_time','')}s</td>"
                f'<td><span class="badge {badge_cls}">{escape(str(e.get("status","")))}</span></td></tr>'
            )

    content = f"""
    <div class="card">
        <h2>Search Command History</h2>
        <form class="search-form" method="GET" action="/search">
            <input type="text" name="command" placeholder="Command type (e.g. PING)" value="{escape(command_q)}">
            <input type="text" name="hostname" placeholder="Hostname / parameter" value="{escape(hostname_q)}">
            <input type="text" name="client_ip" placeholder="Client IP" value="{escape(ip_q)}">
            <button type="submit">Search</button>
        </form>
        <table>
            <tr><th>Time</th><th>Client IP</th><th>Command</th><th>Parameter</th><th>Execution Time</th><th>Status</th></tr>
            {rows_html}
        </table>
    </div>
    """
    return _layout("Search", "/search", content)


# --------------------------------------------------------- Error pages
def error_page(code, message):
    content = f"""
    <div class="card" style="text-align:center;">
        <p class="error-code">{code}</p>
        <h2>{escape(STATUS_TITLES.get(code, 'Error'))}</h2>
        <p>{escape(message)}</p>
        <p><a href="/home">Return to Home</a></p>
    </div>
    """
    return _layout(f"{code} {STATUS_TITLES.get(code, 'Error')}", "", content)


def not_found_page():
    return error_page(404, "The page you requested does not exist on this server.")


STATUS_TITLES = {
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error",
}
