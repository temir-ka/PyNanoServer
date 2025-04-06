

class AuthService:
    def __init__(self, session_manager):
        self.session_manager = session_manager
    
    def login(self, username, response_headers):
        session_id = self.session_manager.create_session(username)
        response_headers.update({"Set-Cookie": f"session_id={session_id}; HttpOnly; Path=/"})

    def _get_session_id(self, request_headers):
        cookie = request_headers.get("Cookie", "")
        session_id = cookie.split("=")[1] if "=" in cookie else None
        return session_id
    
    def is_authenticated(self, request_headers):
        session_id = self._get_session_id(request_headers)
        return self.session_manager.get_user(session_id) is not None
    
    def logout(self, request_headers):
        session_id = self._get_cookie_session()
        self.session_manager.delete_session(session_id)