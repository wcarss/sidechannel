from app import app
from flask import render_template
from lib import x11r5, giphy

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/make')
def make():
    return render_template('make.html')

@app.route('/view')
def view():
#    sentence = x11r5.get_quote()
    sentence = "just a joke sentence"
    return render_template('view.html',
        sentence=sentence,
        background=giphy.GiphyAPI.get_random_image_url())
