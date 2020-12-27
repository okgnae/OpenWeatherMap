# pip3.exe install requests
# https://home.openweathermap.org/api_keys | Default | 522ca5bd15c43b2338651b71c7ceea24
import requests
import json
import datetime
import socket
import pymongo
import time

api_key = '522ca5bd15c43b2338651b71c7ceea24'
city_name = 'Kuwait'
units = 'imperial'

SERVER = '127.0.0.1'
PORT = 1025

def parse_weather(response_json):
    timestamp = datetime.datetime.utcnow().timestamp()
    country_code = response_json['sys']['country']
    city_name = response_json['name']
    weather_description = response_json['weather'][0]['description']
    weather_temp = response_json['main']['temp']
    
    return {
        'TimeStamp': timestamp,
        'Country':country_code,
        'City':city_name,
        'Description':weather_description,
        'Tempature':weather_temp
        }

def get_weather(api_key, city_name, units):
    return parse_weather(json.loads(requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units={units}").content))

def send_weather():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["weather"]
    mycol = mydb["weather"]
    mycol.insert_one(get_weather(api_key, city_name, units))

while True:
    send_weather()
    time.sleep(300)
    
