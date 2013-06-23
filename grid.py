#!/usr/bin/python

import math
import csv

class Location:
    def __init__(self,name,lat,lon,data):
        self.name=name
        self.location=(float(lat),float(lon))
        self.data=[]
        for pack in data:
            if pack:
                self.data.append(pack.upper())
    def __repr__(self):
        return self.name + "-" + str(self.location) 
def readInput():
    inputData=[]
    with open('data.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            name = row[0]+row[1]
            lat = row[2]
            lon = row[3]
            data=row[4:]
            x = Location(name,lat,lon,data)
            inputData.append(x)
    return inputData

def distance(lat1,lon1,lat2,lon2):
    R=6371.0
    dLat = deg2rad(lat2-lat1)
    dLon = deg2rad(lon2-lon1) 
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def deg2rad(deg):
    return deg * (math.pi/180)

from collections import defaultdict

def pivotData(data):
    groups=defaultdict(set)
    for location in data:
        for pack in location.data:
            groups[pack].add(location)
    return groups


data=readInput()
packs= pivotData(data)
for (x,y) in packs.iteritems():
    print str(x) + "-- " + str(y)

minlon=100000
maxlon=-10000
minlat=100000
maxlat=-10000
for l in data:
    minlat = min(minlat,l.location[0])
    minlon = min(minlon,l.location[1])
    maxlat = max(maxlat,l.location[0])
    maxlon = max(maxlon,l.location[1])

print (minlat,minlon,maxlat,maxlon)
print distance(minlat,minlon,maxlat,maxlon)
