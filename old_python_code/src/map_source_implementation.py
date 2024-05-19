from abc import ABC, abstractmethod
from map import Map
from typing import Any, Dict
from map_info import MapInfo

class MapSourceImplementation(ABC):
    @abstractmethod
    def __init__(self, source_json: Dict[str, Any]):
        pass

    @abstractmethod
    def get_map(self, map_info: MapInfo) -> Map:
        pass