import pytest

# from api import API
from rizz_wsgi.api import API
from rizz_wsgi.middleware import Middleware
# from middleware import Middleware


FILE_DIR = "css"
FILE_NAME = "main.css"
FILE_CONTENTS = "body {background-color: red}"


def _create_static(static_dir):
    asset = static_dir.mkdir(FILE_DIR).join(FILE_NAME)
    asset.write(FILE_CONTENTS)
    return asset


@pytest.fixture
def api():
    return API(templates_dir="tests/templates", static_dir="tests/static")


@pytest.fixture
def client(api):
    return api.test_session()


def test_basic_route_adding(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"


def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(req, resp):
            resp.text = "YOLO"


def test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS SO COOL"

    @api.route("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    response = client.get("http://testserver/hey")
    assert response.text == RESPONSE_TEXT


def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/alex").text == "hey alex"
    assert client.get("http://testserver/ben").text == "hey ben"


def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")
    assert response.status_code == 404
    assert response.text == "Not found."


def test_class_based_handler_get(api, client):
    RESPONSE_TEXT = "this is a get request"

    @api.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = RESPONSE_TEXT

    assert client.get("http://testserver/book").text == RESPONSE_TEXT


def test_class_based_handler_post(api, client):
    RESPONSE_TEXT = "this is a post request"

    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = RESPONSE_TEXT

    assert client.post("http://testserver/book").text == RESPONSE_TEXT


def test_class_based_handler_not_allowed_method(api, client):
    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = "yolo"

    with pytest.raises(AttributeError):
        client.get("http://testserver/book")


def test_alternative_route(api, client):
    RESPONSE_TEXT = "Alternative way to add a route"

    def home(req, resp):
        resp.text = RESPONSE_TEXT

    api.add_route("/alternative", home)

    assert client.get("http://testserver/alternative").text == RESPONSE_TEXT


def test_template(api, client):
    @api.route("/html")
    def html_handler(req, resp):
        resp.body = api.template(
            "index.html", context={"title": "Some Title", "name": "Some Name"}
        ).encode()

    response = client.get("http://testserver/html")
    assert "text/html" in response.headers["Content-Type"]
    assert "Some Title" in response.text
    assert "Some Name" in response.text


def test_custom_exception_handler(api, client):
    def on_exception(req, resp, exc):
        resp.text = "Oops! AttributeErrorHappened"

    api.add_exception_handler(on_exception)

    @api.route("/exception")
    def exception_throwing_handler(req, resp):
        raise AttributeError()

    response = client.get("http://testserver/exception")
    assert response.text == "Oops! AttributeErrorHappened"


def test_404_is_returned_for_non_existent_static_file(client):
    assert client.get("http://testserver/main.css").status_code == 404


def test_assets_are_served(tmpdir_factory):
    static_dir = tmpdir_factory.mktemp("static")
    _create_static(static_dir)

    api = API(static_dir=str(static_dir))
    client = api.test_session()
    static_url = f"http://testserver/static/{FILE_DIR}/{FILE_NAME}"
    response = client.get(static_url)
    assert response.status_code == 200
    assert response.text == FILE_CONTENTS


def test_middleware_methods_are_called(api, client):
    process_request_called = False

    process_response_called = False

    class CallMiddlewareMethods(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def process_request(self, request):
            nonlocal process_request_called
            process_request_called = True

        def process_response(self, request, response):
            nonlocal process_response_called
            process_response_called = True

    api.add_middleware(CallMiddlewareMethods)

    @api.route("/")
    def index(request, response):
        response.text = "YOLO"

    client.get("http://testserver")

    assert process_request_called is True
    assert process_response_called is True


def test_allowed_methods_for_function_based_handlers(api, client):
    @api.route("/home", allowed_methods=["post"])
    def home(request, response):
        response.text = "Hey"

    with pytest.raises(AttributeError):
        client.get("http://testserver/home")

    assert client.post("http://testserver/home").text == "Hey"


def test_json_response_helper(api, client):
    @api.route("/json")
    def json_handler(request, response):
        response.json = {"name": "Rizz"}

    response = client.get("http://testserver/json")
    json_body = response.json()
    assert response.headers["Content-Type"] == "application/json"
    assert json_body["name"] == "Rizz"


def test_html_response_helper(api, client):
    @api.route("/html")
    def html_handler(request, response):
        response.html = api.template(
            "index.html",
            context={"title": "Another, Title", "name": "Another, Banger"}
        )

    response = client.get("http://testserver/html")

    assert "text/html" in response.headers["Content-Type"]
    assert "Another, Title" in response.text
    assert "Another, Banger" in response.text


def test_text_response_helper(api, client):
    response_text = "Plain Text"

    @api.route("/text")
    def text_handler(request, response):
        response.text = response_text

    response = client.get("http://testserver/text")

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == response.text


def test_manually_setting_body(api, client):
    @api.route("/body")
    def text_handler(request, response):
        response.body = b"Byte Body"
        response.content_type = "text/plain"

    response = client.get("http://testserver/body")

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == "Byte Body"
