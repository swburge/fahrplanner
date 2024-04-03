import requests
import json
from datetime import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import gmtime, strftime
import re
from collections import OrderedDict
from itertools import islice

class getBusTimes:
    def __init__(self,stopLocation):
        self.stopLocation = stopLocation

    def getNextBus(self):
        smart_token = '3fbb6e859dae87981012497889bc5dfa5b98b1c7'
        headers = {
            'Authorization': f'Token {smart_token}'
        }

        stopLocation = self.stopLocation
        print("stoplocation is:", stopLocation)
        stopLocationList = []
        if stopLocation == "Fowlmere":
            stopLocationList = ['0500SFOWL002','0500SFOWL003']
            #stopLocationList = ['0500CCITY294','0500FOWL002']
            print("stopList is:", stopLocationList)
        else:
            print ("No location, defaulting to Cambridge")

        current = datetime.now()
        request_time = current.strftime("%Y-%m-%dT%H:%M:%S")
        time_join = "&datetime_from="
        time_url = f"{time_join}{request_time}"
        
        #time_url = f"&datetime_from="{request_time}
        base_url = 'https://smartcambridge.org/api/v1/transport/journeys_by_time_and_stop/?stop_id='
        bus_dict = {}
        nextBus = {}
        for stop in stopLocationList:
            request_url = f"{base_url}{stop}{time_url}"
            print(request_url)
            

            response = requests.get (request_url, headers = headers)

            if response.status_code == 200:
                bus_data = response.json()
                
                #print (pretty_json)
                #print(bus_data["results"][0])
                try:
                    nextBus = bus_data["results"][0]
                except IndexError:
                    print("No more buses today")
                
                try:
                    secondBus = bus_data["results"][1]
                except IndexError:
                    print("")
                for journey in bus_data["results"][:2]:
                    new_key =f"{len(bus_dict)+1} bus"
                    if journey["journey_pattern"]["direction"] == 'inbound':
                        destination = journey["journey_pattern"]["service"]["standard_origin"],
                        origin = journey["journey_pattern"]["service"]["standard_destination"]
                    
                    elif journey["journey_pattern"]["direction"] == 'outbound':
                        destination = journey["journey_pattern"]["service"]["standard_destination"],
                        origin = journey["journey_pattern"]["service"]["standard_origin"]
                    
                    bus_dict[new_key] = {
                        "time": journey["time"][:-3],
                        "serviceNumber": journey["journey_pattern"]["service"]["line"]["line_name"],
                        "destination": re.sub(r'[^a-zA-Z]', '', str(destination)),  
                        "origin": origin,
                        "direction": journey["journey_pattern"]["direction"]
                    }
                    #print(bus_dict)
                    #if not bus_dict:
                    #    bus_dict['message'] = 'No more buses today'
            else:
                print(f"Failed to fetch data: {response.status_code}")
        if not bus_dict:
            bus_dict['message'] = "No more buses today"
            return bus_dict
        number_of_buses = len(bus_dict)
        
        print("dictionary contains:", number_of_buses)
        #sorted_dict = dict(sorted(bus_dict.items(), key=lambda bus: bus['time'])) 
        sorted_buses = sorted(bus_dict.items(), key=lambda x: x[1]['time'])
        sorted_buses_dict = OrderedDict(sorted_buses)
       #print (sorted_buses_dict)
        first_two_buses = dict(islice(sorted_buses_dict.items(), 2))
        #print(first_two_buses)
        if not first_two_buses:
            print("no first 2 buses, returning",bus_dict)
            #return bus_dict
        else:
            return first_two_buses


