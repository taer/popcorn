#!/usr/bin/python
import random
from collections import defaultdict

import math
import csv
DISTANCE=10
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
            spamwriter.writerow((row.name,)+row.location+tuple(row.data))
def distance(location1,location2):
    lat1,lon1 = location1
    lat2,lon2 = location2

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


class Spot:
    def __init__(self,name,pos,location):
        self.name=name
        self.location=location
        self.pos=pos
    def __repr__(self):
        return self.name + "-" + str(self.location) 

class PackData:
    def __init__(self,name):
        self.name=name
        self.places=set()
        self.lon=0
        self.lat=0
        self.count=0
    def updateLocation(self,location):
        self.lat = self.lat+location[0]
        self.lon = self.lon+location[1]
        self.count=self.count+1
    def getLocation(self):
        return (self.lat/self.count , self.lon/self.count)
    def __repr__(self):
        return self.name + "-" + str(self.getLocation()) + "-" + str(self.places) 
def pivotData(data):
    groups={}
    for row in data:
        for pack in row.data:
            if pack:
                if pack not in groups:
                    groups[pack]=PackData(pack)
                groups[pack].places.add(row.name)
                groups[pack].updateLocation(row.location)

    return groups

def packParticipated(slot,packData):
    return slot.name in packData.places
def packClose(slot,packData):
    if random.randint(0,100) < 5:
        return distance(slot.location,packData.getLocation()) < DISTANCE
    return False

def isSlotDesired(slot,packdata):
    return packParticipated(slot,packdata) or packClose(slot,packdata) or random.randint(0,500) < 5

def findASlotForPack(packData,availables):
    #print len(availables)
    #print packData.name
    slot = availables.pop(0)
    x=0
    while not isSlotDesired(slot, packData):
        x=x+1
        availables.append(slot)
        slot = availables.pop(0)
    return slot


def boundingBox(inputData):
    minlon=100000
    maxlon=-10000
    minlat=100000
    maxlat=-10000
    for l in inputData:
        minlat = min(minlat,l.location[0])
        minlon = min(minlon,l.location[1])
        maxlat = max(maxlat,l.location[0])
        maxlon = max(maxlon,l.location[1])

    return ( (minlat,minlon),(maxlat,maxlon))

data=readInput('data.csv')
newGrid=readInput('next.csv')
packs= pivotData(data)

cox= boundingBox(data)
print cox
print distance(cox[0],cox[1])
output={}
availables=[]
for loc in newGrid:
    output[loc.name]=loc
    for i,spot in enumerate(loc.data):
        if spot=="O":
            availables.append(Spot(loc.name, i,loc.location))
random.shuffle(availables)
packlist = list(packs.keys())


while availables:
    pack =packlist.pop(0)
    #print "filling pack " + pack
    slot = findASlotForPack(packs[pack],availables)
    packlist.append(pack)
    output[slot.name].data[slot.pos]=pack
    #print slot


writeout('foo.csv',output.itervalues())
