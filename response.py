class Response:
    def __init__(self) -> None:
        self.json = None
        self.html = None
        self.text = None
        self.content_type = None
        self.body = b""
        self.status_code