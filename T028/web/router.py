"""
router.py
---------
Parses a raw HTTP request, decides which page to serve (or which error
status code to return), and builds the final response bytes.

Handles the required status codes:
    200 OK              - a known, well-formed GET request
    400 Bad Request     - malformed request line / unsupported method
    403 Forbidden       - attempt to access a restricted internal path
    404 Not Found       - unknown route (custom 404 page)
"""

from urllib.parse import urlparse, parse_qs

from web.http_utils import build_response
from web import pages

FORBIDDEN_PREFIXES = ("/data", "/config", "/server", "/core", "/client", "/web", "/logs")


def route_request(request_text, config, logger, stats):
    lines = request_text.split("\r\n")
    request_line = lines[0] if lines else ""
    parts = request_line.split(" ")

    # --- 400 Bad Request: malformed request line -----------------------------
    if len(parts) != 3 or not parts[0] or not parts[1]:
        return build_response(400, pages.error_page(400, "Malformed HTTP request line."))

    method, raw_path, http_version = parts

    if not http_version.upper().startswith("HTTP/"):
        return build_response(400, pages.error_page(400, "Malformed HTTP version."))

    # --- 400 Bad Request: unsupported method ----------------------------------
    if method != "GET":
        return build_response(400, pages.error_page(400, f"Unsupported HTTP method: {method}. Only GET is supported."))

    parsed = urlparse(raw_path)
    clean_path = parsed.path.rstrip("/") or "/"
    query = parse_qs(parsed.query)

    # --- 403 Forbidden: path traversal or access to internal project dirs ----
    if ".." in raw_path or clean_path.lower().startswith(FORBIDDEN_PREFIXES):
        return build_response(403, pages.error_page(403, "Access to this resource is forbidden."))

    # --- Routing ---------------------------------------------------------------
    if clean_path in ("/", "/home"):
        return build_response(200, pages.home_page(config))

    if clean_path == "/dashboard":
        return build_response(200, pages.dashboard_page(stats))

    if clean_path == "/history":
        entries = logger.read_all()
        return build_response(200, pages.history_page(entries))

    if clean_path == "/statistics":
        return build_response(200, pages.statistics_page(stats))

    if clean_path == "/search":
        entries = logger.read_all()
        return build_response(200, pages.search_page(entries, query))

    if clean_path == "/download":
        content = logger.raw_bytes()
        if not content:
            return build_response(404, pages.error_page(404, "Log file is empty or not found."))
        return build_response(
            200, content,
            content_type="text/plain; charset=utf-8",
            extra_headers={"Content-Disposition": "attachment; filename=server.log"},
        )

    # --- 404 Not Found: unknown route -------------------------------------------
    return build_response(404, pages.not_found_page())
