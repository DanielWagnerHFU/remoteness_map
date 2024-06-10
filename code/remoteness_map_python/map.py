from overpass_api_client import OverpassAPIClient
from pyproj import Transformer
import requests
import cv2
import numpy as np

class Map:
    def __init__(self, width, lat_min, long_min, lat_max, long_max):
        src_crs = 'EPSG:4326'  # WGS 84
        dst_crs = 'EPSG:3857'  # Web Mercator
        self.coordinate_transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)
        self.coordinate_transformer_reverse = Transformer.from_crs(dst_crs, src_crs, always_xy=True)
        #mercator projection 
        self.bounding_box_min_wgs84 = (lat_min, long_min)
        self.bounding_box_max_wgs84 = (lat_max, long_max)
        self.bounding_box_min_mercator = (x_min, y_min) = self.coordinate_transformer.transform(long_min, lat_min)
        self.bounding_box_max_mercator = (x_max, y_max) = self.coordinate_transformer.transform(long_max, lat_max)
        #downscale factor to map size
        self.scale= width / (x_max- x_min)
        #map size
        self.width = int(width)
        self.height = int(self.scale * (y_max - y_min))
        #init data
        geojson = self.get_geojson()
        self.map_layers = self.generate_mapdata(geojson)
        cv2.imshow('Map', self.map_layers['footway'])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def generate_mapdata(self, geojson):
        way_types = self.get_way_types(geojson)
        map_layers = dict()
        for way_type in way_types:
            map_layers[way_type] = np.zeros((self.height, self.width), dtype=np.uint8)

        for element in geojson['elements']:
            polyline = []
            for point in element['geometry']:
                x, y = self.coordinate_transformer.transform(point['lon'], point['lat'])
                x_ , y_ = x - self.bounding_box_min_mercator[0], self.bounding_box_max_mercator[1] - y
                x__, y__ = self.scale * x_, self.scale * y_
                polyline.append((int(x__), int(y__)))
            way_type = element['tags']['highway']
            layer_matrix = map_layers[way_type]
            cv2.polylines(layer_matrix, [np.array(polyline)], isClosed=False, color=(255), thickness=1)
        return map_layers

    def get_way_types(self, geojson):
        way_types_set = set()
        for element in geojson['elements']:
            way_types_set.add(element['tags']['highway'])
        return list(way_types_set)


    def get_geojson(self):
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = """
        [out:json];
        way({},{},{},{})[highway];
        out geom;
        """
        formatted_query = query.format(self.bounding_box_min_wgs84[0], self.bounding_box_min_wgs84[1], self.bounding_box_max_wgs84[0], self.bounding_box_max_wgs84[1])
        response = requests.get(overpass_url, params={'data': formatted_query})
        return response.json()



if __name__ == "__main__":
    map: Map = Map(1000, 48.195651758475506, 8.7195352489608, 48.33115535177915, 8.983512222877913)