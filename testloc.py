from shapely.geometry import Point, Polygon

'''polygon_coords = [
    (78.645331, 10.863341),
    (78.645578, 10.865279),
    (78.651146, 10.863466),
    (78.650899, 10.861823)
]'''

'''polygon_coords = [
                (10.863341,78.645331),
                (10.865279,78.645578),
                (10.863466,78.651146),
                (10.861823,78.650899)
            ]'''

polygon_coords = [ (10.835588,78.688335),
                (10.836252,78.687853),
                (10.836852,78.687949),
                (10.837126,78.688346),
                (10.837021,78.689355),
                (10.836473,78.690052),
                (10.83562,78.689677),
                (10.835198,78.689473)
            ]
fence = Polygon(polygon_coords)

# Example intruding point (lon, lat)78.647000, 10.863900
point = Point(10.836396,78.689255)

if fence.contains(point):
    print("Detected inside polygon")
else:
    print("Outside polygon")
