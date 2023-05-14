from data_manager import DataManager
from query_manager import QueryManager
from remoteness_map import RemotenessMap

qm = QueryManager()
dm = DataManager()
qm.load_querys()
data = qm.execute_query("all",3000,48.051536,8.206198)
dm.add_data("all", data)
dm.save_data_to_file("all", "all.json")
dm.load_data_from_file("all", "all.json")
gdf = dm.get_geodataframe_from_data("all")
rm = RemotenessMap(gdf)
rm.generate_distance_plot(resolution = 0.01)




