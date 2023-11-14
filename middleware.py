class Middleware:
    def __init__(self, app) -> None:
        self.app = app

    def add(self, middeware_cls):
        self.app = middeware_cls(self.app)

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass

    def handle_request(self, request):
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)

        return response
