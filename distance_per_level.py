#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from math import radians, cos, sin, asin, sqrt


def distance(start, end):
    lat1 = start['lat']
    lon1 = start['lon']
    lat2 = end['lat']
    lon2 = end['lon']
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    m = 6367000 * c
    return m


url = 'http://overpass-api.de/api/interpreter?'
# url += 'data=[out:json];(area["ref:INSEE"="22030"]->.zone;'
url += 'data=[out:json];(area["ref:FR:SIREN"="200065928"]->.zone;'
url += 'way(area.zone)["class:bicycle:commute"~"."];'
url += 'node(area.zone)["class:bicycle:commute"~"."];'
url += ');'
url += 'out meta;>;out meta;'

req = requests.get(url)
data = json.loads(req.text)
dict_name = {}

# Create the nodes dictionnary
nodes = {}
for elt in data['elements']:
    if elt['type'] == 'node':
        node_id = elt['id']
        nodes[node_id] = {}
        nodes[node_id]['lat'] = elt['lat']
        nodes[node_id]['lon'] = elt['lon']

# Compute distance for each way and creates a way dict
# Compute distance for each way and creates a way dict
ways = {}
for elt in data['elements']:
    if elt['type'] == 'way':
        way_distance = 0.0
        for i in range(1, len(elt['nodes'])):
            start = nodes[elt['nodes'][i-1]]
            end = nodes[elt['nodes'][i]]
            way_distance += distance(start, end)
        way_id = elt['id']
        ways[way_id] = {}
        ways[way_id]['distance'] = way_distance
        commute = elt['tags']['class:bicycle:commute']
        if commute in ['-2', '-1', '0', '1', '2']:
            ways[way_id]['commute'] = int(commute)

# Compute distances per commute level
total_distance = 0
distances = [0, 0, 0, 0, 0]
for way in ways:
    total_distance += ways[way]['distance']
    try:
        distances[ways[way]['commute']+2] += ways[way]['distance']
    except:
        pass
print total_distance

print distances
