import urllib

def parse_request(self, request):
    parts = request.split("\r\n\r\n", 1)
    headers = parse_headers(parts[0])
    content_length = int(headers.get("Content-Length", 0))
    body = None
    if content_length:
        body = parse_body(parts[1], headers.get("Content-Type", None))
    return headers, body
    
def parse_headers(self, raw_headers):
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
    
def parse_body(self, raw_body, content_type):
    body = None
    if content_type == "application/x-www-form-urlencoded":
        body = dict(urllib.parse.parse_qsl(raw_body))
    return body