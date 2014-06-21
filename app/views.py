from app import app
from flask import render_template
from lib import x11r5, giphy
import random

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/make')
def make():
    return render_template('make.html')

@app.route('/view')
def view():
    sentence = x11r5.get_quote(length=10)
    words = sentence.split(" ")
    num_words = len(words)
    first_part = " ".join(words[0:num_words/2])
    second_part = " ".join(words[num_words/2+1:])
    #sentence = "just a joke sentence"
    return render_template('view.html',
        #first_part="AND THEN,",
        first_part=first_part,
        #second_part="WE ALL GOT QUIET",
        second_part=second_part,
        sentence=sentence,
        background=giphy.GiphyAPI.get_random_image_url(random.choice(words)))
#        background="http://s3.amazonaws.com/giphymedia/media/w1mf0wmjYN5Yc/giphy.gif")
