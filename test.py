from flask import Flask
import pytest

def test_app():
    app = Flask(__name__)
    app.testing = True

    @app.route("/")
    def hello():
        return "Hello World!"

    # app.run() # this actually works here...
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == "Hello World!"
    print response.headers
    
    assert False
