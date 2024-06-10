import numpy as np
from pyproj import Proj, transform
import matplotlib.pyplot as plt

bounds = [[48.26666056432782, 8.8326872670595], [48.28782586542801, 8.873957456581033]]

in_proj = Proj(init='epsg:4326')  # Geographic coordinate system (longitude, latitude)
out_proj = Proj(init='epsg:3857')  # Web Mercator projection (meters)


x1, y1 = transform(in_proj, out_proj, bounds[0][0], bounds[0][1])
x2, y2 = transform(in_proj, out_proj, bounds[1][0], bounds[1][1])

print(x1, y1)
print(x2, y2)







