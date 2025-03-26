import uuid

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, username):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = username
        return session_id
    
    def get_user(self, session_id):
        user = None
        if session_id in self.sessions:
            user = self.sessions[session_id]
        return user
    
    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]