from threading import RLock

from app.city.city_map import CityMap
import logging

from app.communication import aws
from app.search.a_star import a_star_search

logging.basicConfig()

aws.connect()
lock = RLock()
city_roads = CityMap()


# create all street nodes in city_map
def build_city(roads_dict):
    lock.acquire()
    try:
        city_roads.create_city(roads_dict)
    finally:
        lock.release()


# update congestion of passed in street node
def update_congestion(message):
    lock.acquire()
    try:
        city_roads.update_congestion(message['road'], message['congestion'])
    finally:
        lock.release()


# calculate shortest path to goal
def calculate_best_route(message):
    lock.acquire()
    try:
        return {'path': a_star_search(city_roads.city_roads[message['start']],
                                      city_roads.city_roads[message['end']])}
    finally:
        lock.release()
