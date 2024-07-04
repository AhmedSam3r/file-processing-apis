from project import app


@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"
