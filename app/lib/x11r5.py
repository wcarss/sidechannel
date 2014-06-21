import requests

def get_quote():
  r = requests.get('http://www.x11r5.com')
  first_part = r.text[r.text.find('class="mainquote">') + len('class="mainquote">'):]
  quote = first_part[:first_part.find("</a>")]
  return quote

if __name__ == '__main__':
  print get_quote()
