class GoogleDensityMap:
    def __init__(self, region, radius, location_provider, anchor_provider):
        pass


"""
anchors : List[Hexagon] = anchor_provider.getAnchors([(50.492333,30.357333), (50.492333,30.357333)], radius)
locations : List[List[GoogleLocation]] = [provider.provide(anchor) : List[GoogleLocation] - for anchor in anchors]
locations_by_type : Dict[Type, List[List[GoogleLocation]]] =

drawings = []
for typed_locations in aggregate_by_type:
    counts_per_hex = aggregator.aggregate(typed_locations : List[List[GoogleLocation]]) : List[int] of size (H, ) count per each hexagon.
    drawings.append(drawer.draw(anchors, counts_per_hex))

for drawing in drawings:
    drawing.show()
    drawing.save("maps/" + type + ".png")

"""
