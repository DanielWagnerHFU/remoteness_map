import numpy as np
import numpy.typing as npt
from map_info import MapInfo

class Map:
    def __init__(self, map_matrix: npt.NDArray[np.float64], map_info: MapInfo):
        if self._validate_map_matrix(map_matrix):
            self.matrix = map_matrix
        else:
            raise ValueError("Invalid map matrix")

    def _validate_map_matrix(self, map_matrix: npt.NDArray[np.float64]) -> bool:
        #TODO
        return True

    
if __name__ == "__main__":
    arr: npt.NDArray[np.float64] = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    map_info: MapInfo = MapInfo("all_ways", {"latitude": 48.26859652235137, "longitude": 8.838723012168243}, {"height_meter": 100, "width_meter": 100})
    Map(arr, map_info)
    