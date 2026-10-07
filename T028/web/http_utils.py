"""
http_utils.py
-------------
Low-level HTTP helpers: status-code text mapping and raw HTTP/1.1
response construction. The whole HTTP server is built on the standard
socket library only, so responses are assembled by hand here.
"""

STATUS_MESSAGES = {
    200: "OK",
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error",
}


def build_response(status_code, body, content_type="text/html; charset=utf-8", extra_headers=None):
    """
    Build a complete raw HTTP/1.1 response (headers + body) as bytes.
    `body` may be a str (will be UTF-8 encoded) or bytes already.
    """
    if isinstance(body, str):
        body = body.encode("utf-8")

    status_text = STATUS_MESSAGES.get(status_code, "Unknown")
    headers = [
        f"HTTP/1.1 {status_code} {status_text}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        "Connection: close",
        "Server: ENCS3320-T028-WebServer",
    ]
    if extra_headers:
        for key, value in extra_headers.items():
            headers.append(f"{key}: {value}")

    header_block = "\r\n".join(headers) + "\r\n\r\n"
    return header_block.encode("utf-8") + body
