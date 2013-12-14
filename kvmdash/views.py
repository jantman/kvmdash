from flask import url_for, render_template, g
from kvmdash import kvmdash
from config import STORAGE_CLASS
from storage import get_storage_api

#url_for('static', filename='favicon.ico')

@kvmdash.route('/')
@kvmdash.route('/index')
@kvmdash.route('/index.html')
@kvmdash.route('/index.htm')
def index():
    print STORAGE_CLASS
    c = get_storage_api(STORAGE_CLASS)
    stor = c()
    hosts = stor.list_hosts()
    return render_template("index.html",
                           title = 'kvmdash',
                           hosts = sorted(hosts))
