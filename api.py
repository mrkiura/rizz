from parse import parse
from webob import Request, Response


class API:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parsed = parse(path, request_path)
            if parsed is not None:
                return handler, parsed.named
        return None, None

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)

        if handler:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def route(self, path):
        if path in self.routes:
            raise AssertionError("Route already defined.")

        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."
