import ast

from app import main

with open('tests/test_data.txt', 'r') as file:
    test_roads = ast.literal_eval(file.read())


# TESTS INCLUDE TESTING FOR city_map.py

def test_build_city():
    main.build_city(test_roads)
    assert main.city_roads.city_roads["Gorgeous Grove W1"].name == test_roads["24"]["name"]


def test_update_congestion():
    main.update_congestion({"road": "Gorgeous Grove W1",
                            "congestion": 1})
    assert main.city_roads.city_roads["Gorgeous Grove W1"].congestion == 1


def test_calculate_best_route():
    assert main.calculate_best_route({
        "start": "Gorgeous Grove W1",
        "end": "Gorgeous Grove W2"
    }) == {"path": [
        "Gorgeous Grove W1",
        "Gorgeous Grove W2"
    ]}
