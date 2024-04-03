from font_fredoka_one import FredokaOne
#from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont
from time import gmtime, strftime
import glob
import os
import time

PATH = os.path.dirname(__file__)

icon_map = {
    "snow": [71, 73, 75, 77, 85, 86],
    "rain": [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82],
    "cloud": [3, 45, 48],
    "sun": [0],
    "storm": [95, 96, 99],
    "wind": [],
    "suncloud": [1,2]
}

icons = {}

class MakeImage:
     def __init__(self,weather,timetable):
          self.weather = weather
          self.route = timetable

     def make_display(self):
          temperature = self.weather["temperature"]
          #windspeed = self.weather["windspeed"]
          weathercode = self.weather["weathercode"]
          print("image weathrcode is:", weathercode)
          degree_symbol = "\u00B0"
          tempString = f"Temperature: {temperature}{degree_symbol}C"

          foo = self.route
          print(foo)
        

          #service = self.route["serviceNumber"]
          #destination = self.route["destination"]
          #bustime = self.route["time"]
          
          #timetable = f"{service}\t\t\t{destination}\t\t\t{bustime}"

          for icon in icon_map:
               if weathercode in icon_map[icon]:
                    print("found it in:", icon)
                    weather_icon = icon
                    #print(weather_icon)
                    break
          img = Image.new("P",(250,122))
          draw = ImageDraw.Draw(img)

          for icon in glob.glob(os.path.join(PATH, "resources/icon-*.png")):
               icon_name = icon.split("icon-")[1].replace(".png", "")
               icon_image = Image.open(icon)
               icons[icon_name] = icon_image
               #print(icons[icon_name])
          
          fontBig = ImageFont.truetype(FredokaOne, 22)
          fontSmall = ImageFont.truetype(FredokaOne, 16)
          datetime = time.strftime("%d/%m/%Y %H:%M")
          draw.rectangle((0, 0, 240, 115), fill=(255,255,255), outline=(0, 0, 0))
          draw.text((10, 10), datetime, 'black', font=fontSmall)
          draw.text ((10,30),str(tempString),font=fontSmall)
          if weather_icon is not None:
               img.paste(icons[weather_icon], (190,5))
          draw.text((10,50),str("Next bus:"), font=fontSmall)
          timetable = ""

          key_to_check = 'message'

          if key_to_check in foo.keys():
               timetable = "No more buses today"
          else:
               for bus in foo.values():
                    timetable += f"{bus['serviceNumber']}\t\t{bus['destination']}\t\t{bus['time']}\n"
               print(timetable)
          
          draw.text((10,70),timetable,font=fontSmall)
          #print("saving image")
          img.save('weather.png')
          return img
              