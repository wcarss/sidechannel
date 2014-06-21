import requests

def get_quote(length=None):
    retries = 4
    for i in range(retries):
        r = requests.get('http://www.x11r5.com')
        first_part = r.text[r.text.find('class="mainquote">') + len('class="mainquote">'):]
        quote = first_part[:first_part.find("</a>")]
        if length is not None:
            quote_length = len(quote.split(" "))
            print "quote_length: %s vs length: %s" % (quote_length, length)
            if quote_length <= length:
                break
    if quote_length > length:
        quote = quote[:length]
    return quote

if __name__ == '__main__':
    print get_quote()
