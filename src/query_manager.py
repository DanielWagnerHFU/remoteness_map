import json
import os
import requests

class QueryManager:
    def __init__(self, path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/overpass_querys/query_dictionary.json")):
        self.path = path
        self.querys = {}
        self.overpass_url = "http://overpass-api.de/api/interpreter"
    
    def save_querys(self):
        json_str = json.dumps(self.querys, indent=4)
        with open(self.path, 'w') as file:
            file.write(json_str)
    
    def load_querys(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as file:
                json_str = file.read()
            self.querys = json.loads(json_str)
        else:
            print(f"No file found at path: {self.path}")
        
        return self.querys
    
    def execute_query(self, query_name, lat_1, long_1, lat_2, long_2):
        data = None
        if query_name not in self.querys:
            raise KeyError(f"Query '{query_name}' not found in the dictionary.")

        query = self.querys[query_name]
        query = query.format(lat_1=lat_1,long_1=long_1,lat_2=lat_2,long_2=long_2)
        try:
            response = requests.get(self.overpass_url, params={"data": query})
            response.raise_for_status()
            data = response.text
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Error executing Overpass query: {e}")
        return data