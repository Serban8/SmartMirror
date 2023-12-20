import requests
import json
import time
import os
from datetime import datetime


API_KEY = 'ItbX5T5mryZnQPEec8NPWQ==quMv0CRpTjzVXDrV'
FACTS_JSON = 'Content/demofacts.json'
TRIVIA_JSON = 'Content/demotrivia.json'
WEATHER_JSON = 'Content/demoweather.json'


def get_data(url: str, filename: str, append: bool = True):
  response = requests.get(url, headers={'X-Api-Key': API_KEY})
  if response.status_code == requests.codes.ok:
      print(response.text)
      if append:
          f = open(filename, "a")
      else:
          f = open(filename, "w")
      f.write(response.text)
      f.close()
  else:
      print("Error:", response.status_code, response.text)


def update_facts():
  limit = 3
  api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
  get_data(api_url, FACTS_JSON)


def update_trivia():
  category = 'general'
  limit = 3
  api_url = 'https://api.api-ninjas.com/v1/trivia?category={}&limit={}'.format(category, limit)
  get_data(api_url, TRIVIA_JSON)


def update_weather():
  city = 'brasov'
  api_url = 'https://api.api-ninjas.com/v1/weather?city={}'.format(city)
  get_data(api_url, WEATHER_JSON, False)


# get all data from trivia JSON - for testing only
def get_all_trivia(filename: str):
  f = open(filename)
  data = json.load(f)

  for i in data:
    print(i['question'])
    print(i['answer'])


# get all data from facts JSON - for testing only
def get_all_facts(filename: str):
  f = open(filename)
  data = json.load(f)

  for i in data:
    print(i['fact'])


def get_weather_details():
  f = open(WEATHER_JSON)
  data = json.load(f)
  res = ''
  res = res + 'Humidity: ' + str(data['humidity'])
  
  data['sunrise'] = datetime.fromtimestamp(data['sunrise']).time().strftime('%H:%M')
  res = res + ' Sunrise: ' + str(data['sunrise'])
  data['sunset'] = datetime.fromtimestamp(data['sunset']).time().strftime('%H:%M')
  res = res + ' Sunset: ' + str(data['sunset'])
  
  return res
      

def get_temperature():
  f = open(WEATHER_JSON)
  data = json.load(f)
  return data['temp']
            

# index value to get current fact and trivia from json file
CURRENT_INDEX = 0
MAX_INDEX = 2


def increment_index():
  global CURRENT_INDEX
  if CURRENT_INDEX < MAX_INDEX:
      CURRENT_INDEX += 1
  else:
      CURRENT_INDEX = 0


def get_fact():
  f = open(FACTS_JSON)
  data = json.load(f)

  return data[CURRENT_INDEX]['fact']


def get_trivia():
  f = open(TRIVIA_JSON)
  data = json.load(f)

  return data[CURRENT_INDEX]['question'] + '?'
  

def get_trivia_answer():
  f = open(TRIVIA_JSON)
  data = json.load(f)
    
  return data[CURRENT_INDEX]['answer']


SLEEP_TIME = 2
def run():
  os.system('clear')
  print(get_fact())
  time.sleep(SLEEP_TIME)

  os.system('clear')
  print(get_trivia())
  time.sleep(SLEEP_TIME)
  print("Answer: " + get_trivia_answer())
  time.sleep(SLEEP_TIME)

  # advance trivia and facts
  global CURRENT_INDEX
  if CURRENT_INDEX < MAX_INDEX:
      CURRENT_INDEX += 1
  else:
      CURRENT_INDEX = 0

  os.system('clear')
  print(get_weather_details())
  #time.sleep(SLEEP_TIME)

def update_all():
    update_facts()
    update_trivia()
    update_weather()
    

#for _ in range(4):    
#  run()
