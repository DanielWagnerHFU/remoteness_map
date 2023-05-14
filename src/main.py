from data_manager import DataManager
from query_manager import QueryManager
from remoteness_map import RemotenessMap
import matplotlib.pyplot as plt
import time
import numpy as np
width = 500
qm = QueryManager()
dm = DataManager()
qm.load_querys()
data = qm.execute_query("interurban_roads",5000,48.051536,8.206198)
dm.add_data("interurban_roads", data)
dm.save_data_to_file("interurban_roads", "interurban_roads.json")
dm.load_data_from_file("interurban_roads", "interurban_roads.json")
gdf = dm.get_geodataframe_from_data("interurban_roads")
rm = RemotenessMap(gdf, width=width)

distances = rm.generate_distance_matrix_efficient()
roads = rm.generate_road_matrix()
overlay = np.copy(distances)

height, width = overlay.shape
crop_width = width // 4
crop_height = height // 4
overlay = overlay[crop_height:-crop_height, crop_width:-crop_width]
roads = roads[crop_height:-crop_height, crop_width:-crop_width]
min_value = np.min(overlay)
max_value = np.max(overlay)

# Rescale the values from 0 to 1
overlay = (overlay - min_value) / (max_value - min_value)
#overlay[roads == 1] = 1

# Plotting the distance map with roads overlaid
fig, ax = plt.subplots(figsize=(10, 10))
im = ax.imshow(overlay, cmap='ocean_r', origin='lower')
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('Distance')
ax.set_title('Distance Map with Roads')

plt.show()






