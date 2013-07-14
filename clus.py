#!/usr/bin/python
import csv,math

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


def foo():
    f = open('/home/robert/popcorn/data.csv', 'r')
    reader = csv.reader(f, delimiter=",")
    geo_locs = []
    for line in reader:
        loc_ = (float(line[2]), float(line[3]))  #tuples for location
        geo_locs.append(loc_)
from cluster import *
#cl = HierarchicalClustering(geo_locs, lambda x,y: distance(x,y))
#print "level 10"
#for goo in  cl.getlevel(1):
    #for p in goo:
        ##print "%s,%s"  % p
    #print ""
#print "level 5"
#print cl.getlevel(5)
from scipy.cluster import vq
def getClustersHier(positions, diameter):
    cl = HierarchicalClustering(positions, lambda x,y: distance(x,y))
    return cl.getlevel(diameter)

def getClustersKmean(positions, diameter):
    cl = KMeansClustering(positions,  distance)
    import scipy.spatial.distance
    import numpy
    maxVar=0
    for x in xrange(2,20):
        
        #print "kmeans ",x
        clusters= cl.getclusters(x)
        for goo in clusters:
            distances= scipy.spatial.distance.pdist(goo, distance)
            if len(distances)>0:
                varience =  numpy.std(distances)
                #average =sum( (x for x in distances))/len(distances)
                #varience = sum((average - value) ** 2 for value in distances) / len(distances)
                maxVar=max(maxVar,varience)

                #print varience
        #print ",ax",maxVar
        if maxVar < diameter:
            return clusters
        maxVar=0
