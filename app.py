from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from functools import wraps
from loadjsonfiles import quotes, authors
from random import choice

app = Flask(__name__)
app.config.from_pyfile("./config.py")

quotes_map = {};

def record_call(id):
  if id not in quotes_map:
    quotes_map[id] = 1
  else:
    quotes_map[id] += 1


def get_quote_author(quote_id):
  
  for author in authors:
    author_quotes_ids = author["quoteIds"]
    for id in author_quotes_ids:
      if (id == quote_id):
        return author["author"]
  return ""


def check_token(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'authorization' not in request.headers:
      return make_response(jsonify({"message": "You are not authorized to use this API!"}), 403)

    token_header = request.headers['authorization']
    auth_token = token_header.split()[1]
    if auth_token != app.config["TOKEN"]:
      return make_response(jsonify({"message": "You are not authorized to use this API!"}), 403)
    return f(*args, **kwargs)
  return decorated



@app.route('/quote/random/', methods=['GET'])
@check_token
def get_random_quote():
  random_quote = choice(quotes)
  random_quote_id = random_quote["id"]
  quote_author_name = get_quote_author(random_quote_id)
  record_call(random_quote_id)


  return {
    "quoteId": random_quote_id,
    "quote": random_quote["quote"],
    "author": quote_author_name,
    "quotes_map": quotes_map
  } , 200