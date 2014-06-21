from app import app

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World!'

@app.route('/make')
def make():
    return 'Make!'

@app.route('/view')
def view():
    return 'View!'
