from app import app
from flask import render_template, url_for
from lib import x11r5, giphy
import random
import datetime
import HTMLParser
import redis

html_parser = HTMLParser.HTMLParser()
redis_client = redis.Redis("localhost")

def new_joke():
    (top, bottom, image_url) = generate_random_joke_pieces()
    joke = save_joke(top, bottom, image_url)
    return joke

def generate_random_joke_pieces():
    sentence = x11r5.get_quote(length=10)
    words = sentence.split(" ")
    num_words = len(words)
    top = " ".join(words[:num_words/2])
    bottom = " ".join(words[num_words/2:])
    image_url = giphy.GiphyAPI.get_random_image_url(random.choice(words))
    return (top, bottom, image_url)

def save_joke(top, bottom, image_url):
    global redis_client
    identifier = redis_client.incr("joke_id")
    joke = {
       'id': identifier,
       'top': top,
       'bottom': bottom,
       'image_url': image_url,
       'time': str(datetime.datetime.now()),
       'channel': "AngelHackTO"
    }
    redis_client.hmset("joke:%s" % identifier, joke)
    return joke

def get_latest_joke():
    global redis_client
    identifier = redis_client.get("joke_id")
    if identifier:
        joke = redis_client.hgetall("joke:%s" % identifier)
    else:
        joke = None
    return joke

def get_joke_by_id(identifier):
    global redis_client
    joke = redis_client.hgetall("joke:%s" % identifier)
    return joke

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/make')
def make():
    return render_template('make.html')

@app.route('/')
@app.route('/view')
def view():
    joke = get_latest_joke()
    time = datetime.datetime.now()
    print joke
    print type(joke)
    # dates like "2014-06-21 20:38:15.191355"
    joke_time = datetime.datetime.strptime(joke['time'], "%Y-%m-%d %H:%M:%S.%f")
    if joke is None or time - joke_time > datetime.timedelta(minutes=3):
        joke = new_joke()

    return render_template('view.html',
        first_part=html_parser.unescape(joke['top']),
        second_part=html_parser.unescape(joke['bottom']),
        background=joke['image_url'])

@app.route('/reset')
def reset():
    new_joke()
    return "okay!"
