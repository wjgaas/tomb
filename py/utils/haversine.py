#!/usr/bin/env python
#coding:utf-8

# compute distance between two gps points.

import sys
import math

def toRadians(degree):
    return degree * math.pi / 180

def haversineDistance(lat1, lon1, lat2, lon2):
    R = 6371 # km
    
    lat_delta = toRadians(lat2 - lat1)
    lon_delta = toRadians(lon2 - lon1)
    
    lat1 = toRadians(lat1)
    lat2 = toRadians(lat2)
    
    a = math.sin(lat_delta/2) * math.sin(lat_delta/2) + math.cos(lat1) * math.cos(lat2) * math.sin(lon_delta/2) * math.sin(lon_delta/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

if __name__ == '__main__':
    lat1 = float(sys.argv[1])
    lon1 = float(sys.argv[2])
    lat2 = float(sys.argv[3])
    lon2 = float(sys.argv[4])

    print haversineDistance(lat1, lon1, lat2, lon2)
