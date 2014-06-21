from app import app
from flask import render_template, url_for
from lib import x11r5, giphy
import random
import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/make')
def make():
    return render_template('make.html')

previous_first_part = "AND THEN"
previous_second_part = "WE ALL WENT QUIET"
last_background = 'static/all_went_quiet.gif'
last_time = datetime.datetime.now()

@app.route('/view')
def view():
    global previous_first_part
    global previous_second_part
    global last_background
    global last_time

    time = datetime.datetime.now()
    if time - last_time > datetime.timedelta(minutes=3):
        last_time = time
        sentence = x11r5.get_quote(length=10)
        words = sentence.split(" ")
        num_words = len(words)
        previous_first_part = " ".join(words[0:num_words/2])
        previous_second_part = " ".join(words[num_words/2+1:])
        last_background=giphy.GiphyAPI.get_random_image_url(random.choice(words))

    background = last_background
    first_part = previous_first_part
    second_part = previous_second_part

    #sentence = "just a joke sentence"

    return render_template('view.html',
        #first_part="AND THEN,",
        first_part=first_part,
        #second_part="WE ALL GOT QUIET",
        second_part=second_part,
        #sentence=sentence,
        background=background)
#        background=giphy.GiphyAPI.get_random_image_url(random.choice(words)))
#        background="http://s3.amazonaws.com/giphymedia/media/w1mf0wmjYN5Yc/giphy.gif")

@app.route('/reset')
def reset():
    global last_time
    last_time = last_time - datetime.timedelta(minutes=4)
    return "okay!"
