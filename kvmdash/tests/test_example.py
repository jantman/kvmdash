from flask import Flask
from kvmdash import kvmdash
from kvmdash import config

import os.path
import pytest

def test_app():
    #kvmdash = Flask(__name__)
    #from kvmdash import views
    kvmdash.testing = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    config.FILESTORAGE_DIR = os.path.join(os.path.abspath(os.path.join(basedir, '../')), 'data')

    # app.run() # this actually works here...
    with kvmdash.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.data == "Hello World!"
        print response.headers
        assert False
