from pathlib import Path
import json
from typing import Any, Dict, List
from map_source import MapSource
from map_info import MapInfo
from map import Map

class MapManager:
    def __init__(self, map_types_json: Dict[str, Any]):
        if map_types_json["info"]["version"] != "0":
            raise ValueError(f"Unhandled json version")
        
        self.map_types_json: Dict[str, Any] = map_types_json
        self.map_sources: Dict[str, MapSource] = {}

    def get_map(self, map_info: MapInfo) -> None:
        map_source: MapSource = self.map_sources[map_info.map_type]
        map: Map = map_source.get_map(map_info)
        print(map)

    def build_map(self, map_info: MapInfo) -> None:
        map_type_json: Dict[str, Any] = self._get_map_type_json(map_info.map_type)
        #TODO foreach map build map source - maype outside of this function in initialization
        map_source: MapSource = MapSource(map_type_json["source"])
        #
        map_source.get_map(map_info)
        print(map_source)

    def _get_map_type_json(self, target_map_type: str) -> Dict[str, Any]:
        types_list_json_union: str | List[Dict[str, Any]] = self.map_types_json.get("types", [])
        types_list_json: List[Dict[str, str]] = (
            [] if isinstance(types_list_json_union, str) else types_list_json_union
        )
        map_type_json: Dict[str, Any] = list(filter(lambda x: x["map_type"] == "all_ways", types_list_json))[0]
        return map_type_json
    
    def initialize_map_sources(self) -> None:
        types_json: List[Dict[str, Any]] = self.map_types_json["types"]
        for type_json in types_json:
            map_source: MapSource = MapSource(type_json["source"])
            self.map_sources[type_json["map_type"]] = map_source

if __name__ == "__main__":
    map_types_path: Path = Path(R"C:\Users\danie\Documents\Git\remoteness_map\data\map_types\map_types.json")
    with open(map_types_path, 'r') as map_types_file:
        map_types_json: Dict[str, Any] = json.load(map_types_file)
        map_manager: MapManager = MapManager(map_types_json)
        map_manager.initialize_map_sources()


        #map_info: MapInfo = MapInfo("all_ways", {"latitude": 48.26859652235137, "longitude": 8.838723012168243}, {"height_meter": 100, "width_meter": 100})
        #map_manager.build_map(map_info)