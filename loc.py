
from shapely.geometry import Point, Polygon
lat="10.863342"
lon="78.645333"
latitude = float(lat)
longitude = float(lon)
point = Point(longitude, latitude)
            

polygon_coords = [
    (10.863341,78.645331),
    (10.865279,78.645578),
    (10.863466,78.651146),
    (10.861823,78.650899)
]
#polygon_coords = coors

polygon = Polygon(polygon_coords)

# Check if the point is inside the polygon
if polygon.contains(point):
    s=1
    print("The point is inside the polygon.")
else:
    s=2
    print("no location")
