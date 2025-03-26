from . import utils

class ResponseBuilder:
    def __init__(self):
        self.server_name = "Socket"

    def send_response(self, conn, status_code, content="", headers=None, session_id=None):
        content_bytes = content.encode()
        content_length = len(content_bytes)

        response_headers = {
            "Server": self.server_name,
            "Date": utils.get_current_date(),
            "Content-Type": "text/html",
            "Cash-Control": "no store",
            "Connection": "keep-alive",
            "Content-Length": str(content_length),
        }

        if headers:
            response_headers.update(headers)
        
        if session_id:
            response_headers["Set-Cookie"] = f"session_id={session_id}; HttpOnly; Path=/"
        
        headers_string = "\r\n".join(f"{key}: {value}" for key, value in response_headers.items())
        
        response = f"HTTP/1.1 {status_code} {self._get_status_text(status_code)}\r\n{headers_string}\r\n\r\n"

        conn.send(response.encode())
        conn.send(content_bytes)

    def _get_status_text(self, status_code):
        status_texts = {
            200: "OK",
            302: "Found",
            404: "Not Found",
            500: "Internal Server Error"
        }
        return status_texts.get(status_code, "Unknown Status")
