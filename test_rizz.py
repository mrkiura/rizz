import pytest

from api import API


FILE_DIR = "css"
FILE_NAME = "main.css"
FILE_CONTENTS = "body {background-color: red}"


def _create_static(static_dir):
    asset = static_dir.mkdir(FILE_DIR).join(FILE_NAME)
    asset.write(FILE_CONTENTS)
    return asset


@pytest.fixture
def api():
    return API()


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
    print("client", client)

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
    assert response.text == "AttributeErrorHappened"


def test_404_is_returned_for_non_existent_static_file(client):
    assert client.get("http://testserver/main.css").status_code == 404


def test_assets_are_served(tmpdir_factory):
    static_dir = tmpdir_factory.mktemp("static")
    _create_static(static_dir)

    api = API(static_dir=str(static_dir))
    client = api.test_session()

    response = client.get(f"http://testserver/{FILE_DIR}/{FILE_NAME}")
    assert response.status_code == 200
    assert response.text == FILE_CONTENTS
