from .response_builder import ResponseBuilder

class RequestHandler:
    def __init__(self, conn, session_manager, router):
        self.conn = conn
        self.session_manager = session_manager
        self.router = router

    def handle_request(self):
        request = self.conn.recv(1024).decode("utf-8", errors="replace")
        #print("Received request: ")
        print(request)
        if not request:
            return 
        #print("Recieved request:\n", request)
        parsed_request = self._parse_request(request)
        route = parsed_request.get("Request-target", None)
        
        handler = self.router.get_handler(route)
        if handler: 
            handler_instance = handler(self.conn, self.session_manager, parsed_request)
            handler_instance.handle()
        else:
            ResponseBuilder().send_response(self.conn, 404, content="Not found")

    def _parse_username_password(self, data):
        pairs = data.split("&")
        parsed_data = {}
        for pair in pairs:
            key, val = pair.split("=")
            parsed_data[key] = val
        username = parsed_data.get("username", "")
        password = parsed_data.get("password", "")
        return username, password

    def _parse_request(self, request):
        fields = request.split('\n')
        fields = [x for x in fields if x]
        req = {}
        start_line = ['Method', 'Request-target', 'Protocol']
        for index, val in enumerate(fields[0].split()):
            req[start_line[index]] = val
        
        for field in fields[1:]:
            if field == '\r':
                break
            elif not field:
                continue
            else:
                key, val = field.split(':', 1)
                req[key.strip()] = val.strip()
        
        if req["Method"] == "POST" and req["Request-target"] == "/auth/login":
            username, password = self._parse_username_password(fields[-1])
            req["username"] = username
            req["password"] = password

        return req