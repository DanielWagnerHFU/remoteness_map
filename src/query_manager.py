from data_manager import DataManager
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
    
    def execute_query(self, query_name, radius, lat, long):
        data = None
        if query_name not in self.querys:
            raise KeyError(f"Query '{query_name}' not found in the dictionary.")

        query = self.querys[query_name]
        query = query.format(radius=radius, lat=lat, long=long)
        try:
            response = requests.get(self.overpass_url, params={"data": query})
            response.raise_for_status()
            data = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Error executing Overpass query: {e}")
        return data
    
def test_query_manager():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/overpass_querys/query_dictionary.json")
    qm = QueryManager(file_path)
    qm.load_querys()
    #print(loaded_dict)
    print("\n")
    print(qm.execute_query("foot_paths",1000,48.051536, 8.206198))

if __name__ == '__main__':
    test_query_manager()
    #pass