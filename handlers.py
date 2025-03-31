import config
from server.response import Response

# class BaseHandler:
#     def __init__(self, session_manager, headers, body):
#         self.server_name = "Socket"
#         self.session_manager = session_manager
#         self.headers = headers
#         self.body = body

#     def generate_response(self, status_code, content="", headers=None, session_id=None):
#         content_bytes = content.encode()
#         content_length = len(content_bytes)

#         response_headers = {
#             "Server": self.server_name,
#             "Date": utils.get_current_date(),
#             "Content-Type": "text/html",
#             "Cash-Control": "no-store",
#             "Content-Length": str(content_length),
#         }

#         if headers:
#             response_headers.update(headers)
        
#         if session_id:
#             response_headers["Set-Cookie"] = f"session_id={session_id}; HttpOnly; Path=/"
        
#         headers_string = "\r\n".join(f"{key}: {value}" for key, value in response_headers.items())
        
#         response = f"HTTP/1.1 {status_code} {self._get_status_text(status_code)}\r\n{headers_string}\r\n\r\n".encode()
#         response += content_bytes

#         return response
    
#     def _get_status_text(self, status_code):
#         status_texts = {
#             200: "OK",
#             302: "Found",
#             404: "Not Found",
#             500: "Internal Server Error"
#         }
#         return status_texts.get(status_code, "Unknown Status")

#     def generate_200(self, content=""):
#         return self.generate_response(200, content)
    
#     def generate_404(self, content="Not found"):
#         return self.generate_response(404, content)
    
#     def generate_302(self, location="/", session_id=None):
#         return self.generate_response(302, headers={"Location": location}, session_id=session_id)

#     def handle(self):
#         raise NotImplementedError
    
class HomeHandler(Response):
    def handle(self):
        if self.is_authenticated():
            return self.render_template("dashboard.html")
        else:
            return self.render_template("home.html")

class AboutHandler(Response):
    def handle(self):
        return self.render_template("about.html")

class AuthHandler(Response):
    def handle(self):
        path = self.headers.get("Path", "")
        
        if path == "/auth":
            return self.render_template("auth.html")
        
        elif path == "/auth/login":
            username = self.body.get("username")
            password = self.body.get("password")
            if username == "krasava" and password == "12345678":
                self.set_cookie_session(username)
                return self.redirect(url="/")
            else:
                return self.redirect(url="auth")
        
        elif path == "/auth/logout":
            self.delete_cookie_session()
            return self.redirect(url="/")

class ProfileHandler(Response):
    def handle(self):
        if self.is_authenticated():
            return self.render_template("profile.html")
        else: 
            return self.redirect(url="/auth")

class DefaultHandler(Response):
    def handle(self):
        return self.NotFoundError()