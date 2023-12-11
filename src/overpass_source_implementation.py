from map_source_implementation import MapSourceImplementation
from map import Map
from typing import Any, Dict
from map_info import MapInfo
from overpass_api_client import OverpassAPIClient

class OverpassSourceImplementation(MapSourceImplementation):


    def __init__(self, source_json: Dict[str, Any]):
        self.overpass_api_client = OverpassAPIClient(source_json["api_endpoint"])
        self.query_scheme = source_json["query_scheme"]

    def get_map(self, map_info: MapInfo) -> Map:
        #TODO
        formatted_query: str = eval(f'f"""{self.query_scheme}"""')
        print(formatted_query)
        return Map()