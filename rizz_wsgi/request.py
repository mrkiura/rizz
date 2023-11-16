from _typeshed.wsgi import WSGIEnvironment
from typing import Any
from webob import Request as WebObRequest


class Request(WebObRequest):
    def __init__(self, environ: WSGIEnvironment, **kw: Any) -> None:
        super().__init__(environ, **kw)
