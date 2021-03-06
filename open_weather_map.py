# https://home.openweathermap.org/api_keys | Default | 
import requests
import json
import datetime
import pymongo
import time

api_key = ''
city_name = 'Kuwait'
units = 'imperial'

def get_weather(api_key, city_name, units):
    return parse_weather(json.loads(requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units={units}").content))

def parse_weather(response_json):
    timestamp = int(datetime.datetime.utcnow().timestamp() * 1000)
    country_code = response_json['sys']['country']
    city_name = response_json['name']
    weather_description = response_json['weather'][0]['description']
    weather_temp = float(response_json['main']['temp'])
    
    return {
        'TimeStamp': timestamp,
        'Country':country_code,
        'City':city_name,
        'Description':weather_description,
        'Tempature':weather_temp
        }

def send_weather():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["weather"]
    mycol = mydb["weather"]
    mycol.insert_one(get_weather(api_key, city_name, units))

def main():
    while True:
        send_weather()
        time.sleep(300)

if __name__ == '__main__':
    main()
