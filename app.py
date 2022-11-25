from flask import Flask
from loadjsonfiles import quotes, authors
from random import choice

app = Flask(__name__)
app.config.from_pyfile("./config.py")


@app.route('/quote/random/', methods=['GET'])
def get_random_quote():
  random_quote = choice(quotes)
  random_quotes_id = random_quote["id"]
  return random_quote