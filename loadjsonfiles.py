import json

quotes = None
authors = None

try:
  with open('./json/quotes.json', 'r') as q:
    quotes = json.load(q)
except IOError:
  print("error in opening quotes.json")

try:
  with open('./json/authors.json', 'r') as a:
    authors = json.load(a)
except:
    print("error in opening authors.json")
