import pytest

from api import API


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
