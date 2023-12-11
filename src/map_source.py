from typing import Any, Dict
from map_info import MapInfo
from map import Map
from map_source_implementation import MapSourceImplementation
from overpass_source_implementation import OverpassSourceImplementation

class MapSource:
    def __init__(self, source_json: Dict[str, Any]):
        self.map_source_implementation: MapSourceImplementation = self._get_implementation(source_json)
            
    def get_map(self, map_info: MapInfo) -> Map:
        return self.map_source_implementation.get_map(map_info)
    
    def _get_implementation(self, source_json: Dict[str, Any]) -> MapSourceImplementation:
        name: str = source_json["name"]
        match name:
            case "overpass api":
                return OverpassSourceImplementation(source_json)
            case _ :
                raise ValueError(f"Unhandled case: {name}")
