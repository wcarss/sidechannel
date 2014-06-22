from app import app
from flask import render_template, url_for, redirect, request
from models.jokes import Jokes
import datetime
import HTMLParser

html_parser = HTMLParser.HTMLParser()

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/make', methods=['GET'])
def make_get():
    return render_template('make.html')

@app.route('/make', methods=['POST'])
def make_post():
    top = request.form['top']
    bottom = request.form['bottom']
    image_url = request.form['image_url']
    if image_url.startswith('url('):
        image_url = image_url[4:-1]
    Jokes.save_joke(top, bottom, image_url)
    return '201: Created'

@app.route('/')
@app.route('/view')
def view():
    joke = Jokes.get_latest_joke()
    time = datetime.datetime.now()
    print joke
    print type(joke)
    if joke is None:
        joke = Jokes.new_joke()
    # dates like "2014-06-21 20:38:15.191355"
    joke_time = datetime.datetime.strptime(joke['time'], "%Y-%m-%d %H:%M:%S.%f")
    if time - joke_time > datetime.timedelta(minutes=3):
        joke = Jokes.new_joke()

    return render_template('view.html',
        first_part=html_parser.unescape(joke['top']),
        second_part=html_parser.unescape(joke['bottom']),
        background=joke['image_url'],
        next=Jokes.get_next_existing_joke(joke['id']),
        previous=Jokes.get_previous_existing_joke(joke['id']))

@app.route('/view/<identifier>')
@app.route('/<identifier>')
def view_by_id(identifier):
    joke = Jokes.get_joke_by_id(identifier)
    return render_template('view.html',
        first_part=html_parser.unescape(joke['top']),
        second_part=html_parser.unescape(joke['bottom']),
        background=joke['image_url'],
        next=Jokes.get_next_existing_joke(joke['id']),
        previous=Jokes.get_previous_existing_joke(joke['id']))

@app.route('/reset')
def reset():
    Jokes.new_joke()
    return "okay!"
