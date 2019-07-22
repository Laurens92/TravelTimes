# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:57:04 2017

@author: Laurens
"""

import googlemaps
import math
import numpy
import matplotlib.pyplot as plt
import pickle
import folium
from folium import plugins
import os
from func import flat2lla


# Input parameters
destination_address = ""
home_address = ""

gmaps = googlemaps.Client(key='PLACE YOUR API KEY HERE')

# Geocoding an address
geocode_destination = gmaps.geocode(destination_address)
lat_destination = geocode_destination[0]['geometry']['location']['lat']
long_destination = geocode_destination[0]['geometry']['location']['lng']

geocode_home = gmaps.geocode(home_address)
lat_home = geocode_home[0]['geometry']['location']['lat']
long_home = geocode_home[0]['geometry']['location']['lng']

f = open('data\TravelTime_20170921_153000.pckl', 'rb')
object = pickle.load(f)
f.close()
     
lat = object[0]
long = object[1]
time = object[2]

# Remove locations with a larger travel time than 30 min
time[time>40] = 100; 

# Plot an image of the travelling time!
cs = plt.contourf(long, lat, time,levels=[-50,0,5,10,15,20,25,30,35,40,45,50,55,60],cmap=plt.cm.jet)  
#cs = plt.contourf(long, lat, time,levels=[-5,0,2,4,6,8,10,12,14,16],cmap=plt.cm.jet) 
# Plot circles with distances

for R in range (20000,30001,5000):
    theta = numpy.arange(-math.pi,math.pi,0.01)
    #theta = numpy.arange(-math.pi,math.pi,0.01)
    
    x = R*numpy.cos(theta)
    y = R*numpy.sin(theta)
    lat_circ, long_circ = flat2lla(y, x, lat_destination, long_destination)
    plt.plot(long_circ, lat_circ,'k',linewidth=0.6)

# Create legend
proxy = [plt.Rectangle((0,0),1,1,fc = pc.get_facecolor()[0]) for pc in cs.collections]

#plt.legend(proxy, ['water',0,5,10,15,20,25,30,35,40,45,50,55,60],prop={'size':6})
plt.legend(proxy, ['water',0,5,10,15,20,25,30,35,40,45,50,55,60],prop={'size':6})

#%%

   
# Create figure    
FileName = os.path.join('data', 'test.png')

plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
plt.margins(0,0)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.savefig(FileName, bbox_inches = 'tight',
    pad_inches = 0,dpi=300)

# Create a map and overlay the image
map_osm = folium.Map(location=[lat_destination,long_destination], zoom_start=10)

folium.Marker([lat_destination,long_destination], popup='Work').add_to(map_osm)
folium.Marker([lat_home,long_home], popup='Home').add_to(map_osm)


plugins.ImageOverlay(
    image=open(FileName, 'br'),
    bounds=[[min(lat), min(long)], [max(lat), max(long)]],
    opacity=0.4,
).add_to(map_osm)

folium.LayerControl().add_to(map_osm)
map_osm.save('TravelTimeMap.html')

"""
TILES:
     |  - "OpenStreetMap"
 |      - "Mapbox Bright" (Limited levels of zoom for free tiles)
 |      - "Mapbox Control Room" (Limited levels of zoom for free tiles)
 |      - "Stamen" (Terrain, Toner, and Watercolor)
 |      - "Cloudmade" (Must pass API key)
 |      - "Mapbox" (Must pass API key)
 |      - "CartoDB" (positron and dark_matter)
 """


