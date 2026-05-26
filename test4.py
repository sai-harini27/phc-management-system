from shapely.geometry import Point, Polygon

# Example: the point to check
latitude = 10.863341
longitude = 78.645331
point = Point(longitude, latitude)  # Note: shapely uses (x, y) = (lon, lat)

# Example polygon (list of (longitude, latitude) tuples)
polygon_coords = [
    (10.863341,78.645331),
    (10.865279,78.645578),
    (10.863466,78.651146),
    (10.861823,78.650899)
]

polygon = Polygon(polygon_coords)

# Check if the point is inside the polygon
if polygon.contains(point):
    print("The point is inside the polygon.")
else:
    print("The point is outside the polygon.")
