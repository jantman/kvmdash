from webapp import kvmdash

#url_for('static', filename='favicon.ico')

@kvmdash.route('/')
def index():
    return "hello world"
