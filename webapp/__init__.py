from flask import Flask

kvmdash = Flask(__name__)
from webapp import views
