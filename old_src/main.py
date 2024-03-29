from data_manager import DataManager
from query_manager import QueryManager
from remoteness_map import RemotenessMap
import matplotlib.pyplot as plt
import time
import numpy as np

radius, lat, long = 2000,48.051536,8.206198


qm = QueryManager()
dm = DataManager()
qm.load_querys()
data = qm.execute_query("interurban_roads",radius, lat, long)
dm.add_data("interurban_roads", data)
dm.save_data_to_file("interurban_roads", "interurban_roads.json")

qm.load_querys()
data = qm.execute_query("city_streets",radius, lat, long)
dm.add_data("city_streets", data)
dm.save_data_to_file("city_streets", "city_streets.json")

qm.load_querys()
data = qm.execute_query("forest_roads",radius, lat, long)
dm.add_data("forest_roads", data)
dm.save_data_to_file("forest_roads", "forest_roads.json")

qm.load_querys()
data = qm.execute_query("foot_paths",radius, lat, long)
dm.add_data("foot_paths", data)
dm.save_data_to_file("foot_paths", "foot_paths.json")

def rescale_matrix(matrix):
    min_value = np.min(matrix)
    max_value = np.max(matrix)
    matrix = (matrix - min_value) / (max_value - min_value)
    return matrix

def helper(name):
    width = 200
    dm.load_data_from_file(name, f"{name}.json")
    gdf = dm.get_geodataframe_from_data(name)
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
    overlay = (overlay - min_value) / (max_value - min_value)
    #overlay[roads == 1] = 1
    return overlay

def plot(matrix):
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(matrix, cmap='ocean_r', origin='lower')
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Distance')
    ax.set_title('Distance Map with Roads')
    plt.show()

interurban_roads = helper("interurban_roads")
city_streets = helper("city_streets")
forest_roads = helper("forest_roads")
foot_paths = helper("foot_paths")

plot(rescale_matrix(city_streets))






