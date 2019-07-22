# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 20:55:59 2017

@author: Laurens
"""

# Flat earth coördinates to latitude, longitude
def flat2lla(N, E, lat0, long0):
    import math
    import numpy
    R = 6378136.6 # meters
    f = 1/298.257223563 # flattening
    
    Rn = R/(1-(2*f - f**2)*(math.sin(lat0*math.pi/180))**2)**0.5
    Rm = Rn * (1-(2*f - f**2))/(1-(2*f - f**2)*(math.sin(lat0*math.pi/180))**2)
    
    temp_lat = numpy.zeros((len(N),len(E)))
    temp_long = numpy.zeros((len(N),len(E)))

    for i in range(0,len(N)):  
        for j in range(0,len(E)):  
            
            dlat = math.atan(1/Rm) * N[i] * 180/math.pi
            temp_lat[i][j] = lat0 + dlat

            dlong = math.atan(1/(Rn*math.cos(lat0*math.pi/180))) * E[j] * 180/math.pi
            temp_long[i][j] = long0 + dlong

    lat = temp_lat[:,0]
    long = temp_long[0,:]

    return lat, long; 