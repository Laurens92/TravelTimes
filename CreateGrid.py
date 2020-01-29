# -*- coding: utf-8 -*-
"""
Created on Tue May 23 20:36:15 2017

@author: Laurens
"""

import googlemaps
import numpy
from datetime import datetime
import pickle
from func import flat2lla
# For installing basemap: https://matplotlib.org/basemap/users/installing.html
from mpl_toolkits.basemap import Basemap # Used to check if coordinate is land
import time

# Input parameters
destination_address = ""

gmaps = googlemaps.Client(key='')

# Choose rectangular or circular grid (distances + resolution)
# Choose mode of transport:  "driving", "walking", "bicycling" or "transit"
TravelMode = "driving"

# Choose time of arrival, use either now or the Epoch time since January 1, 1970
TimeOfArrival = 'now'
#TimeOfDeparture = int(time.mktime(time.strptime('2017-09-21 16:30:00', '%Y-%m-%d %H:%M:%S')))
TimeOfDeparture= 'now'

# in kilometers (max 2,500 requests per day)
xwidth = 40
ywidth = 40
resolution = 2

# Compute the grid around the destination
x = numpy.arange(-xwidth,xwidth+1,resolution)*1000
y = numpy.arange(-ywidth,ywidth+1,resolution)*1000

# Calculate the total number of points
NumberOfPoints = len(x)*len(y)

# Geocoding an address
geocode_destination = gmaps.geocode(destination_address)
lat_destination = geocode_destination[0]['geometry']['location']['lat']
long_destination = geocode_destination[0]['geometry']['location']['lng']

# Converting the x-, y-coordinates to latitude and longitude
lat, long = flat2lla(y, x, lat_destination, long_destination)

# Create a basemap
map = Basemap(
        area_thresh=10,
        resolution="h",
        llcrnrlon=min(long-1.0),   # Lower left corner longitude
        llcrnrlat=min(lat-1.0), # Lower left corner latitude
        urcrnrlon=max(long+1.0),  # Upper Right corner longitude
        urcrnrlat=max(lat+1.0)    # Upper Right corner latitude
        )

# Allocate memory
TravelTime = numpy.zeros((len(lat),len(long)))


k = 0;
# Compute the travel time around the destination address
for i in range(0,len(lat)):
    for j in range(0,len(long)):
        # Create lat long coordinates

        address = str([lat[i],long[j]])
        address = address[:-1]
        address = address[1:]

        now = datetime.now()

        # Only calculate the travel time if the coordinates are on land
        if map.is_land(long[j],lat[i]):
            # Request directions via driving
            # Specify arrival time instead of departure time
            # "driving", "walking", "bicycling" or "transit"

            #directions_result = gmaps.directions(address,
            #                             destination_address,
            #                             mode=TravelMode,
            #                             arrival_time=TimeOfArrival,
            #                             avoid="ferries")

            directions_result = gmaps.directions(address,
                                         destination_address,
                                         mode=TravelMode,
                                         departure_time = TimeOfDeparture,
                                         traffic_model = "best_guess",
                                         #arrival_time=TimeOfArrival,
                                         avoid="ferries")

            # Set TravelTime to zero in case the result is empty
            if not directions_result:
                TravelTime[i][j] = 0
            else:
                time_dur_s = directions_result[0]['legs'][0]['duration']['value']
                time_dur_min = time_dur_s/60
                TravelTime[i][j] = time_dur_min
        else:   # When the coordinates are not at land, set travel time to zero
            TravelTime[i][j] = -50

        # print(time_dur_min)
        k = k + 1
        Percentage = "{0:.1f}".format(k/NumberOfPoints*100)
        print(Percentage + ' %')



# Store the data in a file
StrName = str(now)
StrName = StrName.replace('-','')
StrName = StrName.replace(' ','_')
StrName = StrName[:-7]
StrName = StrName.replace(':','')
StrName = StrName.replace(':','')
StrName = 'TravelTime_' + StrName + '.pckl'

f = open(StrName, 'wb')
object = pickle.dump([lat, long, TravelTime],f)
f.close()
