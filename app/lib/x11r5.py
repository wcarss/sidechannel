import requests
import HTMLParser

html_parser = HTMLParser.HTMLParser()

def get_quote(length=None):
    global html_parser
    retries = 4
    for i in range(retries):
        r = requests.get('http://www.x11r5.com')
        first_part = r.text[r.text.find('class="mainquote">') + len('class="mainquote">'):]
        quote = first_part[:first_part.find("</a>")]
        if length is not None:
            quote_length = len(quote.split(" "))
            if quote_length <= length:
                break
    return html_parser.unescape(quote)

if __name__ == '__main__':
    print get_quote()
