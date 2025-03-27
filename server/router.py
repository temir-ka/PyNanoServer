

class Router:
    def __init__(self):
        self.routes = {}
        self.default_handler = None

    def add_route(self, path, handler):
        self.routes[path] = handler
    
    def get_handler(self, path):
        return self.routes.get(path, self.default_handler)
    
    def establish_default_handler(self, handler):
        self.default_handler = handler
    


