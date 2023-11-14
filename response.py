from typing import Any
from webob import Response as WebObResponse


class Response:
    def __init__(self) -> None:
        self.json = None
        self.html = None
        self.text = None
        self.content_type = None
        self.body = b""
        self.status_code = 200

    def __call__(self, environ, start_response) -> Any:
        response = WebObResponse(
            body=self.body,
            content_type=self.content_type,
            status=self.status_code
        )
        return response(environ, start_response)
