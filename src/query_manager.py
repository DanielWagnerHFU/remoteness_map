from data_manager import DataManager
import json
import os

class QueryManager:
    def __init__(self, path):
        self.path = path
        self.dictionary = {}
    
    def save_dictionary(self):
        json_str = json.dumps(self.dictionary)
        with open(self.path, 'w') as file:
            file.write(json_str)
    
    def load_dictionary(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as file:
                json_str = file.read()
            self.dictionary = json.loads(json_str)
        else:
            print(f"No file found at path: {self.path}")
        
        return self.dictionary