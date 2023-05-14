import requests
import os
from shapely.geometry import LineString
import json
import geopandas as gpd

class DataManager:
    def __init__(self, folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/openstreetmap")):
        self.overpass_url = "http://overpass-api.de/api/interpreter"
        self.data = {}
        self.data_storage_path = folder_path

    def add_data(self, name, data):
        self.data[name] = data

    def get_highway_data_from_query(self, name, overpass_query):
        response = requests.get(self.overpass_url, params={"data": overpass_query})
        self.data[name] = response.text

    def save_data_to_file(self, name, filename):
        if name in self.data:
            file_path = os.path.join(self.data_storage_path, filename)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.data[name])
        else:
            raise ValueError("Data with the specified name is missing. Load data before using this method.")
        
    def load_data_from_file(self, name, filename):
        file_path = os.path.join(self.data_storage_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data[name] = file.read()
    
    def get_geodataframe_from_data(self, name):
        if name in self.data:
            data_json = json.loads(self.data[name])
            features = []
            for element in data_json["elements"]:
                if element["type"] == "way" and "geometry" in element:
                    coords = [(point["lon"], point["lat"]) for point in element["geometry"]]
                    line = LineString(coords)
                    feature = {
                        "geometry": line,
                        "properties": element["tags"]
                    }
                    features.append(feature)
            gdf = gpd.GeoDataFrame.from_features(features)
            target_crs = 'EPSG:32632'
            gdf.crs = 'EPSG:4326'
            gdf_projected = gdf.to_crs(target_crs)
            return gdf_projected
        else:
            raise ValueError("Data with the specified name is missing. Load data before using this method.")


