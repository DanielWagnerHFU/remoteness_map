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
        formatted_query: str = self.query_scheme.format(radius = map_info.height_meter, lat = map_info.latitude, long = map_info.longitude)
        map_data: str = self.overpass_api_client.execute_query(formatted_query)
        return Map(map_data)