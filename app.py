from flask import Flask
from loadjsonfiles import quotes, authors
from random import choice

app = Flask(__name__)
app.config.from_pyfile("./config.py")

def get_quote_author(quote_id):
  
  for author in authors:
    author_quotes_ids = author["quoteIds"]
    for id in author_quotes_ids:
      if (id == quote_id):
        return author["author"]
  return ""


@app.route('/quote/random/', methods=['GET'])
def get_random_quote():
  random_quote = choice(quotes)
  random_quote_id = random_quote["id"]
  quote_author_name = get_quote_author(random_quote_id)

  return {
    "quoteId": random_quote_id,
    "quote": random_quote["quote"],
    "author": quote_author_name
  } , 200