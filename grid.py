#!/usr/bin/python

import math
import csv

class Location:
    def __init__(self,name,lat,lon,data):
        self.name=name
        self.location=(float(lat),float(lon))
        self.data=[]
        for pack in data:
            self.data.append(pack.upper())
    def __repr__(self):
        return self.name + "-" + str(self.location) 
def readInput(filename):
    inputData=[]
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            name = row[0]+row[1]
            lat = row[2]
            lon = row[3]
            data=row[4:]
            x = Location(name,lat,lon,data)
            inputData.append(x)
    return inputData
def writeout(filename,data):
    with open(filename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            spamwriter.writerow(row)
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

class Spot:
    def __init__(self,name,pos):
        self.name=name
        self.pos=pos
    def __repr__(self):
        return self.name + "-" + str(self.pos) 


def pivotData(data):
    groups=defaultdict(set)
    for location in data:
        for pack in location.data:
            if pack:
                groups[pack].add(location)
    return groups


data=readInput('data.csv')
newGrid=readInput('next.csv')
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

print distance(minlat,minlon,maxlat,maxlon)

availables=[]
for loc in newGrid:
    for i,spot in enumerate(loc.data):
        if spot=="O":
            availables.append(Spot(loc.name, i))
import random
while availables:
    x= random.choice(availables)
    print x
    print len(availables)
    availables.remove(x)

print availables
writeout('foo.csv',[['hi','hi'],[1,2]])
