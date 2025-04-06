from . import utils

class Response:
    def __init__(self):
        self.response_headers = {
            "Server": "Socket",
            "Date": lambda: utils.get_current_date(),
            "Content-Type": "text/html",
            "Cash-Control": "no-store",
            "Content-Length": "0",
        }

    def to_http(self, status_code, content="", headers=None):
        content_bytes = content.encode()
        content_length = len(content_bytes)

        if headers:
            self.response_headers.update(headers)
        
        if content:
            self.response_headers.update({"Content-Length": str(content_length)})
        
        headers_string = "\r\n".join(f"{key}: {value() if callable(value) else value}" for key, value in self.response_headers.items())
        response = f"HTTP/1.1 {status_code} {self.__get_status_text(status_code)}\r\n{headers_string}\r\n\r\n".encode()
        response += content_bytes

        return response
    
    def __get_status_text(self, status_code):
        status_texts = {
            200: "OK",
            302: "Found",
            404: "Not Found",
            500: "Internal Server Error"
        }
        return status_texts.get(status_code, "Unknown Status")


def render_template(response, template_dir, file_name):
    content = ""
    with open(f"{template_dir}/{file_name}") as file:
        content = file.read()
    return response.to_http(200, content)

def redirect(response, path):
    response.to_http(302, headers={"Location": path})

