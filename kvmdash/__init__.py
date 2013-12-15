from flask import Flask, g

kvmdash = Flask(__name__)
kvmdash.config.from_object('kvmdash.config')

from kvmdash import views
from kvmdash import clientapi_v1
