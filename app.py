from api import API


app = API()


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/tell/{age:d}")
def show_age(request, response, age):
    response.text = f"Age {age}"


@app.route("/type/{var:s}")
def show_type(request, response, var):
    var = "this is a ".join(str(type(var)))

    response.text = f"type: {var}"


@app.route("/template")
def template_handler(request, response):
    response.body = app.template(
        "index.html",
        context={"title": "Rizz Home", "name": "Rizz"}
    ).encode()


@app.route("/sum/{num_1:d}/{num_2:d}")
def sum(request, response, num_1, num_2):
    response.text = f"{num_1} + {num_2} = {num_1 + num_2}"


@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be used.")


def handler(request, response):
    response.text = "Sample handler"


def custom_exception_handler(request, response, exception_cls):
    response.body = app.template(
        "error.html",
        context={
            "title": "Error",
            "message": str(exception_cls)
        }).encode()


app.add_exception_handler(custom_exception_handler)


@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"


class PrintMiddleware(Middleware):
    def process_request(self, request):
        print("Processing request", request.url)

app.add_route("/sample", handler)
