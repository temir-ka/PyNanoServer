import urllib.parse
from .request_parser import parse_request

class RequestHandler:
    def __init__(self, request, session_manager, router, config):
        self.request = request
        self.session_manager = session_manager
        self.router = router
        self.config = config

    def handle_request(self):
        headers, body = parse_request(self.request)
        route = headers.get("Path", None)
        
        handler = self.router.get_handler(route)
        return handler(self.session_manager, self.config, headers, body).handle()