from typing import Dict

class MapInfo:
    def __init__(self, map_type: str, geolocation: Dict[str, float], dimensions: Dict[str, float]):
        self.map_type: str = map_type
        self.latitude: float = geolocation["latitude"]
        self.longitude: float = geolocation["longitude"]
        self.width_meter: float = dimensions["width_meter"]
        self.height_meter: float = dimensions["height_meter"]
        