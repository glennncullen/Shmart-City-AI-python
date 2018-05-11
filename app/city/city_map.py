from app.city.street_node import StreetNode


class CityMap:
    def __init__(self):
        self.city_roads = {}

    def create_city(self, roads_dict):
        for entry in roads_dict:
            road = roads_dict[entry]
            self.city_roads[road['name']] = StreetNode(road['name'], road['lights'], road['position'], road['congestion'])

        for e in roads_dict:
            entry = roads_dict[e]
            road = self.city_roads[entry['name']]
            if entry['straight'] is not None:
                road.straight = self.city_roads[entry['straight']]
            if entry['left'] is not None:
                road.left = self.city_roads[entry['left']]
            if entry['right'] is not None:
                road.right = self.city_roads[entry['right']]

    def update_congestion(self, road, congestion):
        if road not in self.city_roads:
            return;
        self.city_roads[road].congestion = congestion
