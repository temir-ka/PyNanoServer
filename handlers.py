from server import utils 
from server.response_builder import ResponseBuilder

class BaseHandler:
    def __init__(self, conn, session_manager, request):
        self.conn = conn
        self.session_manager = session_manager
        self.request = request
        self.response_builder = ResponseBuilder()

    def handle(self):
        raise NotImplementedError
    
class HomeHandler(BaseHandler):
    def handle(self):
        session_id = self.request["Cookie"].split("=")[1]
        if self.session_manager.get_user(session_id):
            content = utils.load_static_file("templates/dashboard.html")
            if content:
                self.response_builder.send_response(self.conn, 200, content)
            else:
                self.response_builder.send_response(self.conn, 404)
        else:
            content = utils.load_static_file("templates/home.html")
            if content:
                self.response_builder.send_response(self.conn, 200, content)
            else:
                self.response_builder.send_response(self.conn, 404)

class AboutHandler(BaseHandler):
    def handle(self):
        content = utils.load_static_file("templates/about.html")
        if content:
            self.response_builder.send_response(self.conn, 200, content)
        else:
            self.response_builder.send_response(self.conn, 404)

class AuthHandler(BaseHandler):
    def handle(self):
        if self.request["Request-target"] == "/auth":
            content = utils.load_static_file("templates/auth.html")
            if content:
                self.response_builder.send_response(self.conn, 200, content)
            else:
                self.response_builder.send_response(self.conn, 404)
        elif self.request["Request-target"] == "/auth/login":
            if self.request.get("username", None) == "krasava" and self.request.get("password", None) == "12345678":
                session_id = self.session_manager.create_session(self.request["username"])
                print("Redirecting...")
                self.response_builder.send_response(self.conn, 302, headers={"Location": "/"}, session_id=session_id)
            else:
                self.response_builder.send_response(self.conn, 302, headers={"Location": "/auth"})
        elif self.request["Request-target"] == "/auth/logout":
            session_id = self.request["Cookie"].split("=")[1]
            if self.session_manager.get_user(session_id):
                self.session_manager.delete_session(session_id)
            self.response_builder.send_response(self.conn, 302, headers={"Location": "/"})

class ProfileHandler(BaseHandler):
    def handle(self):
        session_id = self.request["Cookie"].split("=")[1]
        print("User: ", self.session_manager.get_user(session_id))
        if self.session_manager.get_user(session_id):
            content = utils.load_static_file("templates/profile.html")
            if content:
                self.response_builder.send_response(self.conn, 200, content)
            else:
                self.response_builder.send_response(self.conn, 404, content="Not found")
        else: 
            self.response_builder.send_response(self.conn, 302, headers={"Location": "/"})