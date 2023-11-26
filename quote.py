import requests
import json


def fetch_meme():
  response = requests.get('https://meme-api.herokuapp.com/gimme')
  data = response.json()
  return data['url']


def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + '\n -' + json_data[0]['a']

  return quote
