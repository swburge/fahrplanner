import glob
import os
import time
import json
import sys
import PIL
from PIL import Image
from collections import OrderedDict

from sys import exit
module_directory = '/Users/burge01/Playground/What_Bus_Display/weather' 
sys.path.append(module_directory)

from weather import WeatherPlugin, my_function
from timetable import getBusTimes
from make_display_image import MakeImage


my_location = 'Fowlmere'

#my_stopLocation = '0500SFOWL002'
#my_stopLocation2 = '0500SFOWL003'
#Addies stop:
#my_stopLocation = '0500CCITY294'


forcast = WeatherPlugin(my_location).show_location()
coordinates = WeatherPlugin(my_location).get_coords()
weather = WeatherPlugin(my_location).get_weather()
timetable = getBusTimes(my_location).getNextBus()
#ßprint(timetable)

#print(f"Next bus: ", timetable["serviceNumber"],timetable["destination"], timetable["time"])

#print(f"Temperature is: ",weather["temperature"],"C")
#weather_image = WeatherPlugin(my_location).make_weather_img()

myImage = MakeImage(weather,timetable).make_display()

img = Image.open("weather.png")
