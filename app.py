from wsgiref.simple_server import make_server
from middleware import Reverseware


def application(environ, start_response):
    response_body = [
        f"{key}: {value}" for key, value in sorted(environ.items())
    ]
    response_body = "\n".join(response_body)
    status = "200 OK"
    response_headers = [
        ("Content-Type", "text/plain"),
    ]
    start_response(status, response_headers)
    return [response_body.encode("utf-8")]


server = make_server("localhost", 8000, app=Reverseware(application))
server.serve_forever()
