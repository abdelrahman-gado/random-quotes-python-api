from flask import Flask

app = Flask(__name__)


@app.route('/quote/random/', methods=['GET'])
def get_random_quote():
  return "Hello world"