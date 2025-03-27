import urllib.parse

class RequestHandler:
    def __init__(self, request, session_manager, router):
        self.request = request
        self.session_manager = session_manager
        self.router = router

    def handle_request(self):
        headers, body = self._parse_request(self.request)
        route = headers.get("Path", None)
        
        handler = self.router.get_handler(route)
        handler_instance = handler(self.session_manager, headers, body)
        return handler_instance.handle()

    def _parse_request(self, request):
        parts = request.split("\r\n\r\n", 1)
        headers = self._parse_headers(parts[0])
        content_length = headers.get("Content-Length", None)
        body = None
        if content_length:
            body = self._parse_body(parts[1], headers.get("Content-Type", None))
        return headers, body
    
    def _parse_headers(self, raw_headers):
        fields = raw_headers.split("\r\n")
        fields = [x for x in fields if x]
        method, path, version = fields[0].split(" ", 2)
        headers = {"Method": method, "Path": path, "Version": version}
            
        for field in fields[1:]:
            if not field:
                continue
            else:
                key, val = field.split(":", 1)
                headers[key.strip()] = val.strip()

        return headers
    
    def _parse_body(self, raw_body, content_type):
        body = None
        if content_type == "application/x-www-form-urlencoded":
            body = dict(urllib.parse.parse_qsl(raw_body))
        return body