from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/make')
def make():
    return render_template('make.html')

@app.route('/view')
def view():
    return render_template('view.html')
