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

last_joke = {
  'top': "AND THEN",
  'bottom': "WE ALL WENT QUIET",
  'image_url': 'static/all_went_quiet.gif'
}
last_time = datetime.datetime.now()

@app.route('/')
@app.route('/view')
def view():
    global last_joke
    global last_time

    time = datetime.datetime.now()
    if time - last_time > datetime.timedelta(minutes=3):
        last_time = time
        (top, bottom, image_url) = generate_random_joke_pieces()
        last_joke = save_joke(top, bottom, image_url, time)

    joke = last_joke

    return render_template('view.html',
        first_part=html_parser.unescape(joke['top']),
        second_part=html_parser.unescape(joke['bottom']),
        background=joke['image_url'])

@app.route('/reset')
def reset():
    global last_time
    last_time = last_time - datetime.timedelta(minutes=4)
    return "okay!"

def generate_random_joke_pieces():
    sentence = x11r5.get_quote(length=10)
    words = sentence.split(" ")
    num_words = len(words)
    top = " ".join(words[:num_words/2])
    bottom = " ".join(words[num_words/2:])
    image_url = giphy.GiphyAPI.get_random_image_url(random.choice(words))
    return (top, bottom, image_url)

def save_joke(top, bottom, image_url, time):
    global redis_client
    identifier = redis_client.incr("joke_id")
    joke = {
       'id': identifier,
       'top': top,
       'bottom': bottom,
       'image_url': image_url,
       'time': str(time),
       'channel': "AngelHackTO"
    }
    redis_client.hmset("joke:%s" % identifier, joke)

    return joke
