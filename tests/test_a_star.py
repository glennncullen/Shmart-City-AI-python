import ast

from app.city.street_node import StreetNode
from app.search.a_star import a_star_search

with open('tests/test_data.txt', 'r') as file:
    test_roads = ast.literal_eval(file.read())

street_node = StreetNode(test_roads["24"]["name"], test_roads["24"]["lights"], test_roads["24"]["position"],
                         test_roads["24"]["congestion"])

test_street = StreetNode(test_roads["25"]["name"], test_roads["25"]["lights"], test_roads["25"]["position"],
                         test_roads["25"]["congestion"])

street_node.straight = test_street

# test a star search
def test_a_star():
    assert a_star_search(street_node, test_street) == [street_node.name, test_street.name]