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


@app.route("/sum/{num_1:d}/{num_2:d}")
def sum(request, response, num_1, num_2):
    response.text = f"{num_1} + {num_2} = {num_1 + num_2}"
