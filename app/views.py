from app import app
from flask import render_template, url_for
from lib import x11r5, giphy
import random
import datetime
import HTMLParser
import redis

html_parser = HTMLParser.HTMLParser()
redis_client = redis.Redis("localhost")
redis_client.set("joke_id", 0)

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

@app.route('/')
@app.route('/view')
def view():
    global previous_first_part
    global previous_second_part
    global last_background
    global last_time
    global redis_client

    time = datetime.datetime.now()
    if time - last_time > datetime.timedelta(minutes=3):
        last_time = time
        sentence = x11r5.get_quote(length=10)
        words = sentence.split(" ")
        num_words = len(words)
        previous_first_part = " ".join(words[0:num_words/2])
        previous_second_part = " ".join(words[num_words/2+1:])
        last_background=giphy.GiphyAPI.get_random_image_url(random.choice(words))
        identifier = redis_client.incr("joke_id")
        joke = {
           'id': identifier,
           'top': previous_first_part,
           'bottom': previous_second_part,
           'image_url': last_background,
           'time': str(last_time),
           'channel': "AngelHackTO"
        }
        redis_client.hmset("joke:%s" % identifier, joke)

    background = last_background
    first_part = html_parser.unescape(previous_first_part)
    second_part = html_parser.unescape(previous_second_part)

    return render_template('view.html',
        first_part=first_part,
        second_part=second_part,
        background=background)

@app.route('/reset')
def reset():
    global last_time
    last_time = last_time - datetime.timedelta(minutes=4)
    return "okay!"
