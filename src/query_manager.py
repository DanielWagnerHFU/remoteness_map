from data_manager import DataManager
import json
import os

class QueryManager:
    def __init__(self, path):
        self.path = path
        self.dictionary = {}
    
    def save_querys(self):
        json_str = json.dumps(self.dictionary)
        with open(self.path, 'w') as file:
            file.write(json_str)
    
    def load_querys(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as file:
                json_str = file.read()
            self.dictionary = json.loads(json_str)
        else:
            print(f"No file found at path: {self.path}")
        
        return self.dictionary
    
def test_query_manager():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/overpass_querys/query_dictionary.json")
    qm = QueryManager(file_path)
    my_dict = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }
    qm.dictionary = my_dict
    qm.save_querys()
    qm.load_querys()
    loaded_dict = qm.dictionary
    print(loaded_dict)

if __name__ == '__main__':
    test_query_manager()
    #pass