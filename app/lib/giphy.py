import json
import random
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
        retries = 2
        for i in range(retries):
            response = requests.get(cls.build_random_url(tag))
#            print json.dumps(response.text, sort_keys=True, indent=4)
            data = json.loads(response.text)['data']
            if not data:
              tag = None
        return data['image_url']

    @classmethod
    def build_search_url(cls, tag=None, api_key=None):
        if api_key is None:
           api_key = "dc6zaTOxFJmzC"
        search_url = "{base_url}{search_endpoint}?api_key={api_key}".format(
            base_url=cls.BASE_URL,
            search_endpoint="search",
            api_key=api_key)
        if tag is not None:
           search_url = "{search_url}&q={tag}&limit=9&offset={offset}".format(
              search_url=search_url,
              tag=tag,
              offset=random.randint(0,2))
        print "this search url was generated: %s" % search_url
        return search_url

    @classmethod
    def get_searched_image_urls(cls, tag):
        retries = 2
        urls = []
        for i in range(retries):
            response = requests.get(cls.build_search_url(tag))
#            print json.dumps(response.text, sort_keys=True, indent=4)
            data = json.loads(response.text)['data']
            if not data:
              tag = None
        for image in data:
            urls.append(image['images']['fixed_height']['url'])

        return {'urls': urls}
 
