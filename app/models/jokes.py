import random
import datetime
import redis
from app.lib import giphy, x11r5

class Jokes(object):
    redis_client = redis.Redis("localhost")

    @classmethod
    def new_joke(cls):
        (top, bottom, image_url) = cls.generate_random_joke_pieces()
        joke = cls.save_joke(top, bottom, image_url)
        return joke

    @classmethod
    def generate_random_joke_pieces(cls):
        sentence = x11r5.get_quote(length=10)
        words = sentence.split(" ")
        num_words = len(words)
        top = " ".join(words[:num_words/2])
        bottom = " ".join(words[num_words/2:])
        image_url = giphy.GiphyAPI.get_random_image_url(random.choice(words))
        return (top, bottom, image_url)

    @classmethod
    def save_joke(cls, top, bottom, image_url):
        identifier = cls.redis_client.incr("joke_id")
        joke = {
           'id': identifier,
           'top': top,
           'bottom': bottom,
           'image_url': image_url,
           'time': str(datetime.datetime.now()),
           'channel': "AngelHackTO"
        }
        cls.redis_client.hmset("joke:%s" % identifier, joke)
        return joke

    @classmethod
    def get_latest_joke(cls):
        identifier = cls.redis_client.get("joke_id")
        if identifier:
            joke = cls.redis_client.hgetall("joke:%s" % identifier)
        else:
            joke = None
        return joke

    @classmethod
    def get_joke_by_id(cls, identifier):
        joke = cls.redis_client.hgetall("joke:%s" % identifier)
        return joke
