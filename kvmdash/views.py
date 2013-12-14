from flask import url_for, render_template
from kvmdash import kvmdash

#url_for('static', filename='favicon.ico')

@kvmdash.route('/')
@kvmdash.route('/index')
@kvmdash.route('/index.html')
@kvmdash.route('/index.htm')
def index():
    return render_template("index.html",
                           title = 'kvmdash')
