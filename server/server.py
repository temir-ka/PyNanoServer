import socket 
from .request_handler import RequestHandler
from .session_manager import SessionManager
from .router import Router

class HTTPServer:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.session_manager = SessionManager()
        self.router = Router()
    
    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Listening on {self.host}:{self.port}")
        
        while True:
            print("Waiting for connection...")
            conn, addr = self.server_socket.accept()
            print(f"Connected by {addr}")

            print(f"Recieving request...")
            request = conn.recv(1024).decode("utf-8", errors="replace")
            
            handler = RequestHandler(request, self.session_manager, self.router)
            
            print("Handling request...")
            response = handler.handle_request()   
            print("Request handled!")
            conn.sendall(response)

            conn.close()
            print("Connection closed.")
