import glob
import os
import time
import json
from sys import exit
import geocoder
import requests
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

from font_fredoka_one import FredokaOne
#from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont
from time import gmtime, strftime



PATH = os.path.dirname(__file__)
# Placeholder variables
windspeed = 0.0
temperature = 0.0
weather_icon = None

def my_function():
    print("Hello from my_function!")

class WeatherPlugin:
     def __init__(self,forcastLocation):
          self.forcastLocation = forcastLocation

     def show_location(self):
          location_string = "{city}, {countrycode}".format(city=self.forcastLocation, countrycode='GB')
          return location_string
     
     def get_coords(self):
          address = self.show_location()
          print(f"address is: ", address)
          g = geocoder.arcgis(address)
          coords = g.latlng
          print(f"coords are:", coords)
          return coords
     def get_weather(self):
          coords = self.get_coords()
          weather = {}
          #res = requests.get("https://api.open-meteo.com/v1/forecast?latitude=" + str(coords[0]) + "&longitude=" + str(coords[1]) + "&current_weather=true")
          #res = requests.get(https://api.open-meteo.com/v1/forecast?latitude=52.0934&longitude=0.0743&hourly=temperature_2m,rain,weather_code,wind_speed_10m&timezone=auto&forecast_days=1)
          #print("https://api.open-meteo.com/v1/forecast?latitude=", str(coords[0]), "&longitude=", str(coords[1]),"&current_weather=true")
          url = "https://api.open-meteo.com/v1/forecast"
          #https://api.open-meteo.com/v1/forecast?latitude=52.0934&longitude=0.0743&current=temperature_2m,weather_code,wind_speed_10m&timezone=auto&forecast_days=1
          #https://api.open-meteo.com/v1/forecast?latitude=52.0934&longitude=0.0743&current=temperature_2m,weather_code&timezone=auto&forecast_days=1
          params = {
	          "latitude": str(coords[0]),
	          "longitude": str(coords[1]),
	          #"hourly": ["temperature_2m", "weather_code"],
               "current": ["temperature_2m","weather_code"],
	          "timezone": "auto",
	          "forecast_days": 1
          }
          responses = openmeteo.weather_api(url, params=params)

          response = responses[0]
          #print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
          #print(f"Elevation {response.Elevation()} m asl")
          #print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
          #print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

          # Process hourly data. The order of variables needs to be the same as requested.
          #hourly = response.Hourly()
          #hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
          #hourly_rain = hourly.Variables(1).ValuesAsNumpy()
          #hourly_weather_code = hourly.Variables(2).ValuesAsNumpy()
          current = response.Current()
          current_temperature_2m = current.Variables(0).Value()
          current_weather_code = current.Variables(1).Value()

          #print(f"Current time {current.Time()}")
          #print(f"Current temperature_2m {current_temperature_2m}")
          #print(f"Current weather_code {current_weather_code}")

          #hourly_data = {"date": pd.date_range(
	     #     start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	     #     end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	     #     freq = pd.Timedelta(seconds = hourly.Interval()),
	     #     inclusive = "left"
          #)}

          current_data = {"date": pd.date_range(
	          start = pd.to_datetime(current.Time(), unit = "s", utc = True),
	          end = pd.to_datetime(current.TimeEnd(), unit = "s", utc = True),
	          freq = pd.Timedelta(seconds = current.Interval()),
	          inclusive = "left"
          )}

         # hourly_data["temperature"] = hourly_temperature_2m
          #hourly_data["rain"] = hourly_rain
          #hourly_data["weathercode"] = hourly_weather_code
          temperature = float(current_temperature_2m)
          #print("temp is:", f'{temperature:.1f}')
        
          current_data["temperature"] = f'{temperature:.1f}'
          current_data["weathercode"] = current_weather_code
          print(current_data)
          return(current_data)
          
        
          
     
              