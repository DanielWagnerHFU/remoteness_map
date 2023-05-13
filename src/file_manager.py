import requests
import os
from shapely.geometry import LineString
import json
import geopandas as gpd

class FileManager:
    def __init__(self):
        self.overpass_url = "http://overpass-api.de/api/interpreter"
        self.data = None
        self.data_storage_path = f"{os.path.dirname(os.path.abspath(__file__))}/../data/"

    def get_highway_data(self, overpass_query):
        response = requests.get(self.overpass_url, params={"data": overpass_query})
        self.data = response.text
        return self.data

    def save_data_to_file(self, filename):
        if self.data is not None:
            with open(f"{self.data_storage_path}\{filename}", 'w') as file:
                file.write(self.data)
        else:
            raise ValueError("Data is missing. Load data into the class before using this method.")
        return self.data
        
    def load_data_from_file(self, filename):
        with open(f"{self.data_storage_path}\{filename}", 'r') as file:
            self.data = file.read()
        return self.data
    
    def get_geodataframe_from_data(self):
        gdf = None
        if self.data is not None:
            data_json = json.loads(self.data)
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
        else:
            raise ValueError("Data is missing. Load data into the class before using this method.")
        return gdf