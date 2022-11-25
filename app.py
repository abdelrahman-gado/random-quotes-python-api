from flask import Flask
from flask import request, jsonify, make_response
from functools import wraps
from loadjsonfiles import quotes, authors
from random import choice
from datetime import datetime
from report import create_report

app = Flask(__name__)
app.config.from_pyfile("./config.py")

calls_count = 0
quotes_map = {};


def get_formatted_current_datetime():
  current_datetime = datetime.now()
  return current_datetime.strftime("%Y_%m_%d_%H_%M_%S")


def record_call(id):
  global calls_count
  
  if id not in quotes_map:
    quotes_map[id] = 1
  else:
    quotes_map[id] += 1
  calls_count += 1


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
  global calls_count

  random_quote = choice(quotes)
  random_quote_id = random_quote["id"]
  quote_author_name = get_quote_author(random_quote_id)

  # record quote in quotes_map dictionary
  record_call(random_quote_id)

  # After every 100 calls, create a report of quotes counts and clear the quotes_map
  if calls_count > app.config["API_CALLS_COUNT"]:
    quotes_list = list(quotes_map.items())
    str_current_date = get_formatted_current_datetime()
    file_path = create_report(quotes_list, str_current_date)
    calls_count = 0

  return {
    "quoteId": random_quote_id,
    "quote": random_quote["quote"],
    "author": quote_author_name
  } , 200