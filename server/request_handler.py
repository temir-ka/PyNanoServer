from .request_parser import parse_request
import inspect

def handle_request(request, router):
    headers, body = parse_request(request.raw_request)
    request.headers, request.body = headers, body
    route = headers.get("Path", None)

    handler = router.get_handler(route)

    def wrapped():
        if "request" in inspect.signature(handler).parameters:
            return handler(request)
        else:
            return handler()

    return wrapped

# class RequestHandler:
#     def __init__(self, request, router):
#         self.request = request
#         self.router = router

#     def handle_request(self):
#         print("Request handler: ", self.request.raw_request)
#         headers, body = parse_request(self.request.raw_request)
#         self.request.headers, self.request.body = headers, body
#         route = headers.get("Path", None)
        
#         handler = self.router.get_handler(route)
#         return handler