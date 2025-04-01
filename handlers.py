import config
from server.response import Response

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
        path = self.request_headers.get("Path", "")
        if self.request_headers["Method"] == "POST":
            if path == "/auth/login":
                username = self.request_body.get("username", None)
                password = self.request_body.get("password", None)
                if username == "krasava" and password == "12345678":
                    self.set_cookie_session(username)
                    return self.redirect(url="/")
                else:
                    return self.redirect(url="/auth")
            
            elif path == "/auth/logout":
                if self.is_authenticated():
                    self.delete_cookie_session()
                return self.redirect(url="/")
        if path == "/auth":
            return self.render_template("auth.html")
        return self.generate_response(404, content="Not found")

class ProfileHandler(Response):
    def handle(self):
        if self.is_authenticated():
            return self.render_template("profile.html")
        else: 
            return self.redirect(url="/auth")

class DefaultHandler(Response):
    def handle(self):
        return self.generate_response(404, content="Not found")