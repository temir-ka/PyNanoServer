from . import utils
import config

class Response:
    def __init__(self, session_manager=None, headers=None, body=None):
        self.response_headers = {
            "Server": "Socket",
            "Date": lambda: utils.get_current_date(),
            "Content-Type": "text/html",
            "Cash-Control": "no-store",
            "Content-Length": "0",
        }
        self.session_manager = session_manager
        self.request_headers = headers
        self.request_body = body

    def generate_response(self, status_code, content="", headers=None):
        content_bytes = content.encode()
        content_length = len(content_bytes)

        if headers:
            self.response_headers.update(headers)
        
        if content:
            self.response_headers.update({"Content-Length": str(content_length)})
        
        headers_string = "\r\n".join(f"{key}: {value() if callable(value) else value}" for key, value in self.response_headers.items())
        response = f"HTTP/1.1 {status_code} {self.__get_status_text(status_code)}\r\n{headers_string}\r\n\r\n".encode()
        print(response)
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

    def get_cookie_session(self):
        cookie = self.request_headers.get("Cookie", "")
        session_id = cookie.split("=")[1] if "=" in cookie else None
        return session_id
    
    def is_authenticated(self):
        session_id = self.get_cookie_session()
        if self.session_manager.get_user(session_id):
            return True
        return False
    
    def set_cookie_session(self, username):
        session_id = self.session_manager.create_session(username)
        self.response_headers.update({"Set-Cookie": f"session_id={session_id}; HttpOnly; Path=/"})
    
    def delete_cookie_session(self):
        session_id = self.get_cookie_session()
        self.session_manager.delete_session(session_id)

    def render_template(self, file_name):
        try:
            with open(f"{config.TEMPLATE_DIR}/{file_name}") as file:
                content = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Template '{file_name}' not found in {config.TEMPLATE_DIR}")

        return self.generate_response(200, content)

    def redirect(self, url):
        return self.generate_response(302, headers={"Location": url})

    def handle(self):
        raise NotImplementedError


            
