import ast
from app.city.street_node import StreetNode

with open('tests/test_data.txt', 'r') as file:
    test_roads = ast.literal_eval(file.read())

street_node = StreetNode(test_roads["24"]["name"], test_roads["24"]["lights"], test_roads["24"]["position"],
                         test_roads["24"]["congestion"])

test_street = StreetNode(test_roads["25"]["name"], test_roads["25"]["lights"], test_roads["25"]["position"],
                         test_roads["25"]["congestion"])


# test connected returns an empty array
def test_get_connected():
    assert all([a == b for a, b in zip(street_node.get_connected(), [])])


# test the cost to road
def test_cost_to_road():
    assert street_node.cost_to_road(test_street) == 175


# test distance
def test_calculate_distance():
    assert street_node.calculate_distance(street_node.position, test_roads["25"]["position"]) == 0.17592017918415534
