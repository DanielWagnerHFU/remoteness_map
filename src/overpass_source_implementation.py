from map_source_implementation import MapSourceImplementation
from map import Map
from typing import Any, Dict
from map_info import MapInfo

class OverpassSourceImplementation(MapSourceImplementation):
    def __init__(self, source_json: Dict[str, Any]):
        #TODO
        pass

    def get_map(self, map_info: MapInfo) -> Map:
        #TODO
        return Map()