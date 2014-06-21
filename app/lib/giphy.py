import json
import requests

class GiphyAPI(object):
    BASE_URL = "http://api.giphy.com/v1/gifs/"

    @classmethod
    def build_random_url(cls, tag=None, api_key=None):
        if api_key is None:
           api_key = "dc6zaTOxFJmzC"
        random_url = "{base_url}{random_endpoint}?api_key={api_key}".format(
            base_url=cls.BASE_URL,
            random_endpoint="random",
            api_key=api_key)
        if tag is not None:
           random_url = "{random_url}&tag={tag}".format(
              random_url=random_url,
              tag=tag)
        print "this random url was generated: %s" % random_url
        return random_url

    @classmethod
    def get_random_image_url(cls, tag=None):
        response = requests.get(cls.build_random_url(tag))
        print json.dumps(response.text, sort_keys=True, indent=4)
        data = json.loads(response.text)['data']
        return data['image_url']
