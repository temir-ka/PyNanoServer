import socket 
from .request_handler import handle_request
from .session_manager import SessionManager
from .router import Router
from .config import Config
from .request import Request

class HTTPServer:
    def __init__(self):
        self.session_manager = SessionManager()
        self.router = Router()
        self.config = Config()
        self.request = Request()
    
    def load_config_from_pyfile(self, path):
        self.config.load_from_pyfile(path)

    def create_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind((self.config["HOST"], self.config["PORT"]))
        except OSError as e:
            raise RuntimeError(f"Cannot bind to {self.config['HOST']}:{self.config['PORT']}")
    
    def run(self):
        self.server_socket.listen()
        print(f"Listening on {self.config['HOST']}:{self.config['PORT']}")
        
        while True:
            print("Waiting for connection...")
            conn, addr = self.server_socket.accept()
            print(f"Connected by {addr}")

            print(f"Recieving request...")
            self.request.raw_request = conn.recv(1024).decode("utf-8", errors="replace")
            
            handler = handle_request(self.request, self.router)
            
            #print("Headers: ", self.request.headers)

            print("Handling request...")
            response = handler()
            print("Request handled!")
            conn.sendall(response)

            conn.close()
            print("Connection closed.")
