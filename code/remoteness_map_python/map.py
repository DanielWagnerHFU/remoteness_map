from typing import Dict, List
from layer import Layer
from overpass_api_client import OverpassAPIClient
from pyproj import Transformer

class Map:
    def __init__(self, bounds, width) -> None:
        self.coordinate_transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
        self.layers: Dict[str, Layer] = {}
        self.width = width
        self.bounds = bounds
        


    def generate_layers_from_json(self, json) -> None:
        pass

    def get_json_for_bounds(self)

    def add_layer(self, unique_name: str, layer: Layer) -> None:
        self.layers.update({unique_name: layer})

    def render(self) -> None:
        for layer_name, layer in self.layers.items():
            print(layer_name, layer)


if __name__ == "__main__":
    map: Map = Map()
    map.add_layer("a", Layer())
    print(map.layers)
    map.render()