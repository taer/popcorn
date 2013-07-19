#!/usr/bin/python
import random
from collections import defaultdict

import math
import csv
class Location:
    def __init__(self,name,addr,lat,lon,data):
        self.name=name
        self.addr=addr
        self.location=(float(lat),float(lon))
        self.data=[]
        for pack in data:
            self.data.append(pack.upper())
    def __repr__(self):
        return self.name + "-" + str(self.location) 
def readInput(filename):
    inputData=[]
    packInfo=[]
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        mode=0
        for row in spamreader:
            if row[0] =="X": 
                pass
            elif row[0]=="Packs":
                mode=1
            elif mode==0:
                name = row[0]
                addr = row[1]
                latlon = row[2].split(",")
                data=row[3:]
                x = Location(name,addr,latlon[0],latlon[1],data)
                inputData.append(x)
            elif mode==1:
                pac=row[0]
                picks=int(row[1])
                packInfo.append( (pac,picks))
    return (inputData,packInfo)

def writeout(filename,headersFrom, data,picks):
    with open(headersFrom, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers=list()
        for row in spamreader:
            if row[0] =="X": 
                headers.append(row)
    with open(filename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in headers:
            spamwriter.writerow(row)

        for row in data:
            spamwriter.writerow((row.name,row.addr,str(row.location[0])+","+str(row.location[1]))+tuple(row.data))
        spamwriter.writerow(("packs","picks"))
        for row in picks:
            spamwriter.writerow(row)
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
import clus
DIAMETER=2 #KM
DISTANCE=3 #KM
class PackData:
    def __init__(self,name):
        self.name=name
        self.places=set()
        self.coor=list()
        self.center=None
    def updateLocation(self,location):
        self.coor.append(location)
    def getLocation(self):
        if self.center:
            return self.center  
        self.center=list()
        clusters = clus.getClustersHier(list(set(self.coor)), DIAMETER)
        maxWeight=0
        for cluster in clusters:
            weight = sum([self.coor.count(x) for x in cluster])
            maxWeight=max(maxWeight,weight)
        for cluster in clusters:
            lon=0
            lat=0
            for point in cluster:
                lon=lon+point[0]
                lat=lat+point[1]
            center = (lon/len(cluster),lat/len(cluster))
            weight = sum([self.coor.count(x) for x in cluster]) / float(maxWeight)
            self.center.append({'center':center, 'weight':weight})

        return self.center
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
    for pack in groups.values():
        pack.getLocation()
    return groups

def packParticipated(slot,packData):
    return slot.name in packData.places
def packClose(slot,packData):
    for center in packData.getLocation():
        cent = center['center']
        weight = center['weight']
        delta= distance(slot.location,cent)
        prob=0
        if weight > 0:
            prob=.2
        if weight >= .2:
            prob=.5
        if weight >= .7:
            prob=1
        if delta < DISTANCE and random.randint(0,10) < prob*10:
            return True
    return False

def isSlotDesired(slot,packdata):
    return packParticipated(slot,packdata) or packClose(slot,packdata) or random.randint(0,500) < 5

def findASlotForPack(packData,availables):
    #print len(availables)
    #print packData.name
    if len(availables)<=0:
        return None
    slot = availables.pop(0)
    x=0
    while not isSlotDesired(slot, packData):
        x=x+1
        availables.append(slot)
        slot = availables.pop(0)
    return slot



def main():
    data,_=readInput('data.csv')
    newGrid,picks=readInput('next.csv')
    packs= pivotData(data)

    output={}
    availables=[]
    for loc in newGrid:
        output[loc.name]=loc
        for i,spot in enumerate(loc.data):
            if spot=="O":
                availables.append(Spot(loc.name, i,loc.location))
    random.shuffle(availables)

    print "filling " + str(len(availables))
    while availables:
        pTuple =picks.pop(0)
        pack,count=pTuple
        #print "filling pack " + pack
        for x in xrange(0,count):
            slot = findASlotForPack(packs[pack],availables)
            if slot:
                output[slot.name].data[slot.pos]=pack
        picks.append(pTuple)
        #print slot

    outVal = sorted(output.itervalues())
    writeout('foo.csv','next.csv', outVal, picks)


if __name__ == "__main__":
    main()
