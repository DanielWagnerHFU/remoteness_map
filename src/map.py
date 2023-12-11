import json


class Map:
    def __init__(self, map_data: str):
        map_json = json.loads(map_data)
        print(map_json)