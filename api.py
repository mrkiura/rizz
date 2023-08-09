from webob import Request, Response


class API:
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        user_agent = request.environ.get("HTTP_USER_AGENT", "No User Agent Found")
        response = Response()
        response.text = f"Hello, my friend with this user agent: {user_agent}"
        return response
