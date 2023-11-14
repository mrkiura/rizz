class Middleware:
    def __init__(self, app) -> None:
        self.app = app

    def add(self, middeware_cls):
        self.app = middeware_cls(self.app)

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass
