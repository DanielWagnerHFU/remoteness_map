import requests
import json
import cv2
import numpy as np
from pyproj import Proj, Transformer, transform, CRS
from pyproj.aoi import AreaOfInterest
import hashlib
import time
import matplotlib.pyplot as plt

lat_min, long_min = 48.195651758475506, 8.7195352489608
lat_max, long_max = 48.33115535177915, 8.983512222877913
proj_wgs84 = Proj(init='epsg:4326')
proj_mercator = Proj(init='epsg:3857')

x_min, y_min = transform(proj_wgs84, proj_mercator, long_min, lat_min)
x_max, y_max = transform(proj_wgs84, proj_mercator, long_max, lat_max)

map_width = 1500
scale_factor = map_width / (x_max- x_min)
map_height = scale_factor * (y_max - y_min)

map_matrix = np.zeros((int(map_height), int(map_width), 3), dtype=np.uint8)

overpass_url = "http://overpass-api.de/api/interpreter"
query = """
[out:json];
way({},{},{},{})[highway];
out geom;
"""
formatted_query = query.format(lat_min, long_min, lat_max, long_max)
response = requests.get(overpass_url, params={'data': formatted_query})
map_data = response.json()
#print(map_data)

transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
def custom_transform(lat, long):
    x, y = transformer.transform(long, lat)
    x_ , y_ = x - x_min, y_max - y
    x__, y__ = scale_factor * x_, scale_factor * y_
    return x__, y__

def string_to_color(string):
    hash_value = hashlib.sha256(string.encode()).hexdigest()
    r = int(hash_value[:2], 16)
    g = int(hash_value[2:4], 16)
    b = int(hash_value[4:6], 16)
    return (r, g, b)

st = time.time()
transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
for element in map_data['elements']:
    for node in element['geometry']:
        x, y = transformer.transform(node['lon'], node['lat'])
        x_ , y_ = x - x_min, y_max - y
        x__, y__ = scale_factor * x_, scale_factor * y_
        #print(x__, y__)
t = time.time()- st
print(f"Elapsed time: {t:.6f} seconds")

st = time.time()
for element in map_data['elements']:
    if element['type'] == 'way' and 'geometry' in element:
        polyline = []
        for node in element['geometry']:
            x, y = custom_transform(node['lat'], node['lon'])
            polyline.append((int(x), int(y)))
        c = (255, 255, 255)
        if 'tags' in element:
            if 'highway' in element['tags']:
                c = string_to_color(element['tags']['highway'])
                print(polyline)
                cv2.polylines(map_matrix, [np.array(polyline)], isClosed=False, color=c, thickness=1)
                #cv2.imshow('Map', map_matrix)
                #cv2.waitKey(1)
cv2.destroyAllWindows()
t = time.time()- st
print(f"Elapsed time: {t:.6f} seconds")

fig, ax = plt.subplots()
ax.imshow(map_matrix)
aspect_ratio = map_matrix.shape[1] / map_matrix.shape[0]
ax.set_aspect(aspect_ratio)
ax.autoscale(enable=True)

plt.show()