from pathlib import Path
import json
from typing import Any, Dict, List

class MapManager:
    def __init__(self, map_types_json: dict[str, Any]):
        self.map_types_json: dict[str, Any] = map_types_json

    def build_map(self, map_type: str, geolocation: dict[str, float], dimensions: dict[str, float]):
        map_type_json: Dict[str, Any] = self._get_map_type_json(map_type)
        print(map_type_json["source"]["name"])

    def _get_map_type_json(self, target_map_type: str) -> Dict[str, Any]:
        types_list_json_union: str | List[Dict[str, Any]] = self.map_types_json.get("types", [])
        types_list_json: List[Dict[str, str]] = (
            [] if isinstance(types_list_json_union, str) else types_list_json_union
        )
        map_type_json: Dict[str, Any] = list(filter(lambda x: x["map_type"] == "all_ways", types_list_json))[0]
        return map_type_json


if __name__ == "__main__":
    map_types_path: Path = Path(R"C:\Users\danie\Documents\Git\remoteness_map\data\map_types\map_types.json")
    with open(map_types_path, 'r') as map_types_file:
        map_types_json: dict[str, Any] = json.load(map_types_file)
        map_manager: MapManager = MapManager(map_types_json)
        map_manager.build_map("all_ways", {"latitude": 48.26859652235137, "longitude": 8.838723012168243}, {"height_meter": 100, "width_meter": 100})