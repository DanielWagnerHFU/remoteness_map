import requests
import os
from shapely.geometry import LineString
import json
import geopandas as gpd

import requests
import os
from shapely.geometry import LineString
import json
import geopandas as gpd

class FileManager:
    def __init__(self):
        self.overpass_url = "http://overpass-api.de/api/interpreter"
        self.data = {}  # Dictionary to store name/data pairs
        self.data_storage_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")

    def get_highway_data(self, name, overpass_query):
        response = requests.get(self.overpass_url, params={"data": overpass_query})
        self.data[name] = response.text

    def save_data_to_file(self, name, filename):
        if name in self.data:
            file_path = os.path.join(self.data_storage_path, filename)
            with open(file_path, 'w') as file:
                file.write(self.data[name])
        else:
            raise ValueError("Data with the specified name is missing. Load data before using this method.")
        
    def load_data_from_file(self, name, filename):
        file_path = os.path.join(self.data_storage_path, filename)
        with open(file_path, 'r') as file:
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
            return gdf
        else:
            raise ValueError("Data with the specified name is missing. Load data before using this method.")

def test_file_manager():
    file_manager = FileManager()
    coordinates = (48.051536, 8.206198)
    radius = 500
    overpass_query = f"[out:json];way(around:{radius}, {coordinates[0]}, {coordinates[1]})[highway];out geom;"
    file_manager.get_highway_data("highway_data", overpass_query)
    file_manager.save_data_to_file("highway_data", "highway_data.json")
    file_manager.load_data_from_file("highway_data", "highway_data.json")
    gdf = file_manager.get_geodataframe_from_data("highway_data")
    print(gdf)

if __name__ == '__main__':
    #test_file_manager()
    pass

