from flask import Flask
from loadjsonfiles import quotes, authors

app = Flask(__name__)
app.config.from_pyfile("./config.py")


@app.route('/quote/random/', methods=['GET'])
def get_random_quote():
  return "Hello world"