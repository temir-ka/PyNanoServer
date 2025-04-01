import socket 
from .request_handler import RequestHandler
from .session_manager import SessionManager
from .router import Router
from .config import Config

class HTTPServer:
    def __init__(self):
        self.session_manager = SessionManager()
        self.router = Router()
        self.config = Config()
    
    def load_config_from_pyfile(self, path):
        try:
            self.config.load_from_pyfile(path)
        except FileNotFoundError:
            raise FileNotFoundError
    
    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind((self.config["HOST"], self.config["PORT"]))
        except OSError as e:
            raise RuntimeError(f"Cannot bind to {self.config['HOST']}:{self.config['PORT']} - {e}")
        
        self.server_socket.listen()
        print(f"Listening on {self.config['HOST']}:{self.config['PORT']}")
        
        while True:
            print("Waiting for connection...")
            conn, addr = self.server_socket.accept()
            print(f"Connected by {addr}")

            print(f"Recieving request...")
            request = conn.recv(1024).decode("utf-8", errors="replace")
            
            handler = RequestHandler(request, self.session_manager, self.router, self.config)
            
            print("Handling request...")
            response = handler.handle_request()   
            print("Request handled!")
            conn.sendall(response)

            conn.close()
            print("Connection closed.")
