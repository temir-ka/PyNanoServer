from server import utils 

class BaseHandler:
    def __init__(self, session_manager, headers, body):
        self.server_name = "Socket"
        self.session_manager = session_manager
        self.headers = headers
        self.body = body

    def generate_response(self, status_code, content="", headers=None, session_id=None):
        content_bytes = content.encode()
        content_length = len(content_bytes)

        response_headers = {
            "Server": self.server_name,
            "Date": utils.get_current_date(),
            "Content-Type": "text/html",
            "Cash-Control": "no store",
            "Content-Length": str(content_length),
        }

        if headers:
            response_headers.update(headers)
        
        if session_id:
            response_headers["Set-Cookie"] = f"session_id={session_id}; HttpOnly; Path=/"
        
        headers_string = "\r\n".join(f"{key}: {value}" for key, value in response_headers.items())
        
        response = f"HTTP/1.1 {status_code} {self._get_status_text(status_code)}\r\n{headers_string}\r\n\r\n".encode()
        response += content_bytes

        return response
    
    def _get_status_text(self, status_code):
        status_texts = {
            200: "OK",
            302: "Found",
            404: "Not Found",
            500: "Internal Server Error"
        }
        return status_texts.get(status_code, "Unknown Status")

    def generate_200(self, content=""):
        return self.generate_response(200, content)
    
    def generate_404(self, content="Not found"):
        return self.generate_response(404, content)
    
    def generate_302(self, location="/", session_id=None):
        return self.generate_response(302, headers={"Location": location}, session_id=session_id)

    def handle(self):
        raise NotImplementedError
    
class HomeHandler(BaseHandler):
    def handle(self):
        session_id = self.headers["Cookie"].split("=")[1]
        if self.session_manager.get_user(session_id):
            content = utils.load_static_file("templates/dashboard.html")
            if content:
                return self.generate_200(content)
            else:
                return self.generate_404()
        else:
            content = utils.load_static_file("templates/home.html")
            if content:
                return self.generate_200(content)
            else:
                return self.generate_404()

class AboutHandler(BaseHandler):
    def handle(self):
        content = utils.load_static_file("templates/about.html")
        if content:
            return self.generate_200(content)
        else:
            return self.generate_404()

class AuthHandler(BaseHandler):
    def handle(self):
        if self.headers["Path"] == "/auth":
            content = utils.load_static_file("templates/auth.html")
            if content:
                return self.generate_200(content)
            else:
                return self.generate_404()
        elif self.headers["Path"] == "/auth/login":
            if self.body.get("username", None) == "krasava" and self.body.get("password", None) == "12345678":
                session_id = self.session_manager.create_session(self.body["username"])
                return self.generate_302(location="/", session_id=session_id)
            else:
                return self.generate_302(location="/auth")
        elif self.headers["Path"] == "/auth/logout":
            session_id = self.headers["Cookie"].split("=")[1]
            if self.session_manager.get_user(session_id):
                self.session_manager.delete_session(session_id)
            return self.generate_302(location="/")

class ProfileHandler(BaseHandler):
    def handle(self):
        session_id = self.headers["Cookie"].split("=")[1]
        if self.session_manager.get_user(session_id):
            content = utils.load_static_file("templates/profile.html")
            if content:
                return self.generate_200(content)
            else:
                return self.generate_404()
        else: 
            return self.generate_302(location="/")

class DefaultHandler(BaseHandler):
    def handle(self):
        return self.generate_404()