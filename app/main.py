from threading import RLock

from app.city.city_map import CityMap
import logging

from app.city.street_node import StreetNode
from app.communication import aws
from app.search.a_star import a_star_search

logging.basicConfig()

aws.connect()
lock = RLock()
city_roads = CityMap()


def build_city(roads_dict):
    lock.acquire()
    try:
        city_roads.create_city(roads_dict)
    finally:
        lock.release()


def update_congestion(message):
    lock.acquire()
    try:
        city_roads.update_congestion(message['road'], message['congestion'])
    finally:
        lock.release()


def calculate_best_route(message):
    lock.acquire()
    try:
        return {'path': a_star_search(city_roads.city_roads[message['start']],
                                      city_roads.city_roads[message['end']])}
    finally:
        lock.release()


# ||            ||
# vv test space vv
#
# entire_city = {u'24':
#                    {u'right': u'New Eggs Drive N3', u'name': u'Gorgeous Grove W1', u'straight': u'Gorgeous Grove W2',
#                     u'lights': False, u'congestion': 0, u'position': {u'y': 141.526337, u'x': 553.7},
#                     u'left': u'New Eggs Drive S5'},
#                u'25': {u'right': None, u'name': u'Gorgeous Grove W2', u'straight': u'Gorgeous Grove W3',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 141.526337, u'x': 450.581238},
#                        u'left': u'Time Capsule Court S1'},
#                u'26': {u'right': None, u'name': u'Gorgeous Grove W3', u'straight': u'Gorgeous Grove W4',
#                        u'lights': True, u'congestion': 0, u'position': {u'y': 143, u'x': 349},
#                        u'left': u'Wrong Way S1'},
#                u'27': {u'right': u'Meaney Avenue N1', u'name': u'Gorgeous Grove W4', u'straight': u'Gorgeous Grove W5',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 141.8, u'x': 249.7}, u'left': None},
#                u'20': {u'right': u'Wrong Way S1', u'name': u'Gorgeous Grove E3', u'straight': u'Gorgeous Grove E4',
#                        u'lights': True, u'congestion': 0, u'position': {u'y': 145.869278, u'x': 169.8}, u'left': None},
#                u'21': {u'right': u'Time Capsule Court S1', u'name': u'Gorgeous Grove E4',
#                        u'straight': u'Gorgeous Grove E5', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 145.869278, u'x': 269.9}, u'left': None},
#                u'22': {u'right': u'New Eggs Drive S5', u'name': u'Gorgeous Grove E5', u'straight': u'Gorgeous Grove E6',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 145.869278, u'x': 368.5},
#                        u'left': u'New Eggs Drive N3'},
#                u'23': {u'right': None, u'name': u'Gorgeous Grove E6', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 145.869278, u'x': 471.7}, u'left': None},
#                u'28': {u'right': u'Capped Bypass N3', u'name': u'Gorgeous Grove W5', u'straight': u'Gorgeous Grove W6',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 141.8, u'x': 150.1},
#                        u'left': u'Capped Bypass S5'},
#                u'29': {u'right': None, u'name': u'Gorgeous Grove W6', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 141.8, u'x': 49.2}, u'left': None},
#                u'0': {u'right': u'Downey Memorial Way W3', u'name': u'Capped Bypass S1',
#                       u'straight': u'Capped Bypass S2', u'lights': False, u'congestion': 0,
#                       u'position': {u'y': 534.7, u'x': 61.0691376}, u'left': u'Downey Memorial Way E2'},
#                u'4': {u'right': u'Gym Fee Freeway W5', u'name': u'Capped Bypass S5', u'straight': u'Capped Bypass S6',
#                       u'lights': False, u'congestion': 0, u'position': {u'y': 135.5, u'x': 61.0691376},
#                       u'left': u'Gym Fee Freeway E2'},
#                u'8': {u'right': u'Resit Row E1', u'name': u'Capped Bypass N3', u'straight': u'Capped Bypass N4',
#                       u'lights': True, u'congestion': 0, u'position': {u'y': 153, u'x': 57.744812}, u'left': None},
#                u'59': {u'right': None, u'name': u'Meaney Avenue S2', u'straight': u'Meaney Avenue S3', u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 437.18, u'x': 159.71},
#                        u'left': u'King Cullen Boulevard E1'},
#                u'58': {u'right': u'Downey Memorial Way W2', u'name': u'Meaney Avenue S1',
#                        u'straight': u'Meaney Avenue S2', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 539.9012, u'x': 159.71}, u'left': u'Downey Memorial Way E3'},
#                u'55': {u'right': None, u'name': u'Man Welly Way N3', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 454.201172, u'x': 356.327332}, u'left': None},
#                u'54': {u'right': u'Massive Road E1', u'name': u'Man Welly Way N2', u'straight': u'Man Welly Way N3',
#                        u'lights': True, u'congestion': 0, u'position': {u'y': 351.6012, u'x': 356.327332},
#                        u'left': None},
#                u'57': {u'right': u'Man Welly Way N3', u'name': u'Massive Road W1', u'straight': None, u'lights': True,
#                        u'congestion': 0, u'position': {u'y': 441.5062, u'x': 450.980835}, u'left': u'Man Welly Way S2'},
#                u'56': {u'right': u'New Eggs Drive S2', u'name': u'Massive Road E1', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 446.122742, u'x': 369.618866},
#                        u'left': u'New Eggs Drive N6'},
#                u'51': {u'right': u'King Cullen Boulevard W3', u'name': u'Man Welly Way S2',
#                        u'straight': u'Man Welly Way S3', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 432.340149, u'x': 362.923767}, u'left': u'King Cullen Boulevard E3'},
#                u'50': {u'right': None, u'name': u'Man Welly Way S1', u'straight': u'Man Welly Way S2', u'lights': True,
#                        u'congestion': 0, u'position': {u'y': 531.321167, u'x': 362.127319},
#                        u'left': u'Massive Road E1'},
#                u'53': {u'right': u'King Cullen Boulevard E3', u'name': u'Man Welly Way N1',
#                        u'straight': u'Man Welly Way N2', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 252.707352, u'x': 357.146729}, u'left': u'King Cullen Boulevard W3'},
#                u'52': {u'right': u'Resit Row W3', u'name': u'Man Welly Way S3', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 330.901184, u'x': 362.923767}, u'left': u'Resit Row E4'},
#                u'88': {u'right': u'Capped Bypass N4', u'name': u'Resit Row W5', u'straight': None, u'lights': True,
#                        u'congestion': 0, u'position': {u'y': 240.8, u'x': 149.2}, u'left': u'Capped Bypass S4'},
#                u'89': {u'right': u'Meaney Avenue S4', u'name': u'Resit Row E1', u'straight': u'Resit Row E2',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 246.8, u'x': 67.3999939},
#                        u'left': u'Meaney Avenue N2'},
#                u'82': {u'right': u'King Cullen Boulevard W4', u'name': u'Reid Street S2',
#                        u'straight': u'Reid Street S3', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 432.480957, u'x': 264.55304}, u'left': u'King Cullen Boulevard E2'},
#                u'83': {u'right': u'Resit Row W4', u'name': u'Reid Street S3', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 332.592316, u'x': 263.745361}, u'left': u'Resit Row E3'},
#                u'80': {u'right': None, u'name': u'Reid Street N3', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 472.6012, u'x': 256.0765}, u'left': None},
#                u'81': {u'right': u'Downey Memorial Way W1', u'name': u'Reid Street S1', u'straight': u'Reid Street S2',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 533.4012, u'x': 264.55304},
#                        u'left': None},
#                u'86': {u'right': u'Reid Street N1', u'name': u'Resit Row W3', u'straight': u'Resit Row W4',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 240.8, u'x': 350.7}, u'left': None},
#                u'87': {u'right': u'Meaney Avenue N2', u'name': u'Resit Row W4', u'straight': u'Resit Row W5',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 240.8, u'x': 250.7419},
#                        u'left': u'Meaney Avenue S4'},
#                u'84': {u'right': u'New Eggs Drive N4', u'name': u'Resit Row W1', u'straight': u'Resit Row W2',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 241.9, u'x': 556.327332},
#                        u'left': u'New Eggs Drive S4'},
#                u'85': {u'right': u'Man Welly Way N1', u'name': u'Resit Row W2', u'straight': u'Resit Row W3',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 241.9, u'x': 451.3}, u'left': None},
#                u'3': {u'right': u'Gorgeous Grove W6', u'name': u'Capped Bypass S4', u'straight': u'Capped Bypass S5',
#                       u'lights': False, u'congestion': 0, u'position': {u'y': 232.8, u'x': 61.0691376},
#                       u'left': u'Gorgeous Grove E2'},
#                u'7': {u'right': u'Gorgeous Grove E2', u'name': u'Capped Bypass N2', u'straight': u'Capped Bypass N3',
#                       u'lights': False, u'congestion': 0, u'position': {u'y': 53.2720947, u'x': 57.744812},
#                       u'left': u'Gorgeous Grove W6'},
#                u'100': {u'right': None, u'name': u"Viper's View W1", u'straight': None, u'lights': False,
#                         u'congestion': 0, u'position': {u'y': 341.759979, u'x': 42.82733}, u'left': None},
#                u'101': {u'right': u'Capped Bypass S3', u'name': u"Viper's View E1", u'straight': None, u'lights': False,
#                         u'congestion': 0, u'position': {u'y': 347.8, u'x': -41.9726868}, u'left': u'Capped Bypass N5'},
#                u'39': {u'right': u'New Eggs Drive S6', u'name': u'Gym Fee Freeway E5', u'straight': None,
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 47, u'x': 371.8},
#                        u'left': u'New Eggs Drive N2'},
#                u'38': {u'right': u'Time Capsule Court S2', u'name': u'Gym Fee Freeway E4',
#                        u'straight': u'Gym Fee Freeway E5', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 47, u'x': 272.4}, u'left': u'Time Capsule Court N2'},
#                u'33': {u'right': u'Capped Bypass N2', u'name': u'Gym Fee Freeway W4',
#                        u'straight': u'Gym Fee Freeway W5', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 42.4, u'x': 150.6}, u'left': u'Capped Bypass S6'},
#                u'32': {u'right': None, u'name': u'Gym Fee Freeway W3', u'straight': u'Gym Fee Freeway W4',
#                        u'lights': True, u'congestion': 0, u'position': {u'y': 42.4, u'x': 250.5},
#                        u'left': u'Hmph Place S1'},
#                u'31': {u'right': u'Wrong Way N1', u'name': u'Gym Fee Freeway W2', u'straight': u'Gym Fee Freeway W3',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 42.4, u'x': 350.5}, u'left': None},
#                u'30': {u'right': u'Time Capsule Court N2', u'name': u'Gym Fee Freeway W1',
#                        u'straight': u'Gym Fee Freeway W2', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 43.0958862, u'x': 451.1538}, u'left': u'Time Capsule Court S2'},
#                u'37': {u'right': None, u'name': u'Gym Fee Freeway E3', u'straight': u'Gym Fee Freeway E4',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 47, u'x': 171.9},
#                        u'left': u'Wrong Way N1'},
#                u'36': {u'right': u'Hmph Place S1', u'name': u'Gym Fee Freeway E2', u'straight': u'Gym Fee Freeway E3',
#                        u'lights': True, u'congestion': 0, u'position': {u'y': 47, u'x': 71.9}, u'left': None},
#                u'35': {u'right': u'Capped Bypass S6', u'name': u'Gym Fee Freeway E1',
#                        u'straight': u'Gym Fee Freeway E2', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 47, u'x': -31}, u'left': u'Capped Bypass N2'},
#                u'34': {u'right': None, u'name': u'Gym Fee Freeway W5', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 42.4, u'x': 49.6}, u'left': None},
#                u'60': {u'right': u'Resit Row W5', u'name': u'Meaney Avenue S3', u'straight': u'Meaney Avenue S4',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 332.817719, u'x': 160.621887},
#                        u'left': u'Resit Row E2'},
#                u'61': {u'right': u'Gorgeous Grove W5', u'name': u'Meaney Avenue S4', u'straight': None,
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 233.4, u'x': 161.8},
#                        u'left': u'Gorgeous Grove E3'},
#                u'62': {u'right': u'Resit Row E2', u'name': u'Meaney Avenue N1', u'straight': u'Meaney Avenue N2',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 155.1, u'x': 155.6},
#                        u'left': u'Resit Row W5'},
#                u'63': {u'right': u'King Cullen Boulevard E1', u'name': u'Meaney Avenue N2',
#                        u'straight': u'Meaney Avenue N3', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 255.41478, u'x': 154.414673}, u'left': None},
#                u'64': {u'right': u'Downey Memorial Way E3', u'name': u'Meaney Avenue N3',
#                        u'straight': u'Meaney Avenue N4', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 353.715363, u'x': 153.312866}, u'left': u'Downey Memorial Way W2'},
#                u'65': {u'right': None, u'name': u'Meaney Avenue N4', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 452.6012, u'x': 153.312866}, u'left': None},
#                u'66': {u'right': u'Massive Road W1', u'name': u'New Eggs Drive S1', u'straight': u'New Eggs Drive S2',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 533.226135, u'x': 464.628235},
#                        u'left': None}, u'67': {u'right': u'King Cullen Boulevard W2', u'name': u'New Eggs Drive S2',
#                                                u'straight': u'New Eggs Drive S3', u'lights': False, u'congestion': 0,
#                                                u'position': {u'y': 434.426147, u'x': 464.628235},
#                                                u'left': u'King Cullen Boulevard E4'},
#                u'68': {u'right': u'Resit Row W2', u'name': u'New Eggs Drive S3', u'straight': u'New Eggs Drive S4',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 335.12616, u'x': 464.628235},
#                        u'left': u'Resit Row E5'},
#                u'69': {u'right': u'Gorgeous Grove W2', u'name': u'New Eggs Drive S4', u'straight': u'New Eggs Drive S5',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 235.426147, u'x': 464.628235},
#                        u'left': u'Gorgeous Grove E6'},
#                u'2': {u'right': None, u'name': u'Capped Bypass S3', u'straight': u'Capped Bypass S4', u'lights': True,
#                       u'congestion': 0, u'position': {u'y': 333.1, u'x': 61.0691376}, u'left': u'Resit Row E1'},
#                u'6': {u'right': u'Gym Fee Freeway E2', u'name': u'Capped Bypass N1', u'straight': u'Capped Bypass N2',
#                       u'lights': False, u'congestion': 0, u'position': {u'y': -48.3, u'x': 57.744812},
#                       u'left': u'Gym Fee Freeway W5'},
#                u'99': {u'right': u'Gorgeous Grove E4', u'name': u'Wrong Way N1', u'straight': None, u'lights': True,
#                        u'congestion': 0, u'position': {u'y': 55.25354, u'x': 257.108826},
#                        u'left': u'Gorgeous Grove W4'},
#                u'98': {u'right': u'Gym Fee Freeway W3', u'name': u'Wrong Way S1', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 134.547424, u'x': 263.496033},
#                        u'left': u'Gym Fee Freeway E4'},
#                u'91': {u'right': None, u'name': u'Resit Row E3', u'straight': u'Resit Row E4', u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 247.38, u'x': 270.93}, u'left': u'Man Welly Way N1'},
#                u'90': {u'right': None, u'name': u'Resit Row E2', u'straight': u'Resit Row E3', u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 247.059479, u'x': 168.602417}, u'left': u'Reid Street N1'},
#                u'93': {u'right': None, u'name': u'Resit Row E5', u'straight': None, u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 247.38, u'x': 473.727325}, u'left': None},
#                u'92': {u'right': u'New Eggs Drive S4', u'name': u'Resit Row E4', u'straight': u'Resit Row E5',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 247.38, u'x': 371},
#                        u'left': u'New Eggs Drive N4'},
#                u'95': {u'right': None, u'name': u'Time Capsule Court S2', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 34.2, u'x': 363.5415}, u'left': None},
#                u'94': {u'right': u'Gym Fee Freeway W2', u'name': u'Time Capsule Court S1',
#                        u'straight': u'Time Capsule Court S2', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 135.900986, u'x': 363.5415}, u'left': u'Gym Fee Freeway E5'},
#                u'97': {u'right': u'Gorgeous Grove E5', u'name': u'Time Capsule Court N2', u'straight': None,
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 55.5197144, u'x': 357.000336},
#                        u'left': u'Gorgeous Grove W3'},
#                u'96': {u'right': u'Gym Fee Freeway E5', u'name': u'Time Capsule Court N1',
#                        u'straight': u'Time Capsule Court N2', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': -45, u'x': 357.000336}, u'left': u'Gym Fee Freeway W2'},
#                u'11': {u'right': None, u'name': u'Capped Bypass N6', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 452.3, u'x': 57.744812}, u'left': None},
#                u'10': {u'right': u'Downey Memorial Way E2', u'name': u'Capped Bypass N5',
#                        u'straight': u'Capped Bypass N6', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 353.1, u'x': 57.744812}, u'left': u'Downey Memorial Way W3'},
#                u'13': {u'right': u'Capped Bypass N6', u'name': u'Downey Memorial Way W2',
#                        u'straight': u'Downey Memorial Way W3', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 441.36, u'x': 149.29}, u'left': u'Capped Bypass S2'},
#                u'12': {u'right': u'Meaney Avenue N4', u'name': u'Downey Memorial Way W1',
#                        u'straight': u'Downey Memorial Way W2', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 441.07, u'x': 253.75}, u'left': u'Meaney Avenue S2'},
#                u'15': {u'right': u'Capped Bypass S2', u'name': u'Downey Memorial Way E1',
#                        u'straight': u'Downey Memorial Way E2', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 447.4, u'x': -41.9726868}, u'left': u'Capped Bypass N6'},
#                u'14': {u'right': None, u'name': u'Downey Memorial Way W3', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 441.36, u'x': 42.82733}, u'left': None},
#                u'17': {u'right': u'Reid Street S2', u'name': u'Downey Memorial Way E3', u'straight': None,
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 447.91, u'x': 166.56},
#                        u'left': u'Reid Street N3'},
#                u'16': {u'right': u'Meaney Avenue S2', u'name': u'Downey Memorial Way E2',
#                        u'straight': u'Downey Memorial Way E3', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 447.4, u'x': 60.8000031}, u'left': u'Meaney Avenue N4'},
#                u'19': {u'right': None, u'name': u'Gorgeous Grove E2', u'straight': u'Gorgeous Grove E3',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 145.869278, u'x': 70.33957},
#                        u'left': u'Meaney Avenue N1'},
#                u'18': {u'right': u'Capped Bypass S5', u'name': u'Gorgeous Grove E1', u'straight': u'Gorgeous Grove E2',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 144.9, u'x': -30.9},
#                        u'left': u'Capped Bypass N3'},
#                u'48': {u'right': u'Reid Street N2', u'name': u'King Cullen Boulevard W3',
#                        u'straight': u'King Cullen Boulevard W4', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 340.215973, u'x': 355.2}, u'left': u'Reid Street S3'},
#                u'49': {u'right': u'Meaney Avenue N3', u'name': u'King Cullen Boulevard W4', u'straight': None,
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 340.215973, u'x': 251.528381},
#                        u'left': u'Meaney Avenue S3'},
#                u'46': {u'right': u'New Eggs Drive N5', u'name': u'King Cullen Boulevard W1',
#                        u'straight': u'King Cullen Boulevard W2', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 340.215973, u'x': 565.827332}, u'left': u'New Eggs Drive S3'},
#                u'47': {u'right': u'Man Welly Way N2', u'name': u'King Cullen Boulevard W2',
#                        u'straight': u'King Cullen Boulevard W3', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 340.215973, u'x': 452.5}, u'left': u'Man Welly Way S3'},
#                u'44': {u'right': u'New Eggs Drive S3', u'name': u'King Cullen Boulevard E3',
#                        u'straight': u'King Cullen Boulevard E4', u'lights': False, u'congestion': 7,
#                        u'position': {u'y': 346.3, u'x': 368.7}, u'left': u'New Eggs Drive N5'},
#                u'45': {u'right': None, u'name': u'King Cullen Boulevard E4', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 346.3, u'x': 472.827332}, u'left': None},
#                u'42': {u'right': u'Reid Street S3', u'name': u'King Cullen Boulevard E1',
#                        u'straight': u'King Cullen Boulevard E2', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 347.2, u'x': 164.9}, u'left': u'Reid Street N2'},
#                u'43': {u'right': u'Man Welly Way S3', u'name': u'King Cullen Boulevard E2',
#                        u'straight': u'King Cullen Boulevard E3', u'lights': False, u'congestion': 7,
#                        u'position': {u'y': 346.3, u'x': 269.3}, u'left': u'Man Welly Way N2'},
#                u'40': {u'right': None, u'name': u'Hmph Place S1', u'straight': None, u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 34.2, u'x': 161.141174}, u'left': None},
#                u'41': {u'right': u'Gym Fee Freeway E3', u'name': u'Hmph Place N1', u'straight': None, u'lights': True,
#                        u'congestion': 0, u'position': {u'y': -45, u'x': 154.6}, u'left': u'Gym Fee Freeway W4'},
#                u'1': {u'right': u"Viper's View W1", u'name': u'Capped Bypass S2', u'straight': u'Capped Bypass S3',
#                       u'lights': False, u'congestion': 0, u'position': {u'y': 433.48, u'x': 61.0691376}, u'left': None},
#                u'5': {u'right': None, u'name': u'Capped Bypass S6', u'straight': None, u'lights': False,
#                       u'congestion': 0, u'position': {u'y': 34.9, u'x': 61.0691376}, u'left': None},
#                u'9': {u'right': None, u'name': u'Capped Bypass N4', u'straight': u'Capped Bypass N5', u'lights': False,
#                       u'congestion': 0, u'position': {u'y': 252.6, u'x': 57.744812}, u'left': u"Viper's View W1"},
#                u'77': {u'right': None, u'name': u'New Eggs Drive N6', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 452.926147, u'x': 457.756653}, u'left': None},
#                u'76': {u'right': None, u'name': u'New Eggs Drive N5', u'straight': u'New Eggs Drive N6',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 354.026154, u'x': 457.756653},
#                        u'left': u'Massive Road W1'},
#                u'75': {u'right': u'King Cullen Boulevard E4', u'name': u'New Eggs Drive N4',
#                        u'straight': u'New Eggs Drive N5', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 254.426147, u'x': 457.756653}, u'left': u'King Cullen Boulevard W2'},
#                u'74': {u'right': u'Resit Row E5', u'name': u'New Eggs Drive N3', u'straight': u'New Eggs Drive N4',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 155.026154, u'x': 457.756653},
#                        u'left': u'Resit Row W2'},
#                u'73': {u'right': u'Gorgeous Grove E6', u'name': u'New Eggs Drive N2', u'straight': u'New Eggs Drive N3',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': 55.7568054, u'x': 457.756653},
#                        u'left': u'Gorgeous Grove W2'},
#                u'72': {u'right': None, u'name': u'New Eggs Drive N1', u'straight': u'New Eggs Drive N2',
#                        u'lights': False, u'congestion': 0, u'position': {u'y': -42.67386, u'x': 457.756653},
#                        u'left': u'Gym Fee Freeway W1'},
#                u'71': {u'right': None, u'name': u'New Eggs Drive S6', u'straight': None, u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 34.32614, u'x': 464.628235}, u'left': None},
#                u'70': {u'right': u'Gym Fee Freeway W1', u'name': u'New Eggs Drive S5',
#                        u'straight': u'New Eggs Drive S6', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 134.026154, u'x': 464.628235}, u'left': None},
#                u'79': {u'right': None, u'name': u'Reid Street N2', u'straight': u'Reid Street N3', u'lights': False,
#                        u'congestion': 0, u'position': {u'y': 369.668243, u'x': 256.0765},
#                        u'left': u'Downey Memorial Way W1'},
#                u'78': {u'right': u'King Cullen Boulevard E2', u'name': u'Reid Street N1',
#                        u'straight': u'Reid Street N2', u'lights': False, u'congestion': 0,
#                        u'position': {u'y': 269.401184, u'x': 256.0765}, u'left': u'King Cullen Boulevard W4'}}



# def test_build_roads_init(roads_dict):
#     for entry in roads_dict:
#         road = roads_dict[entry]
#         city_roads[road['name']] = StreetNode(road['name'], road['lights'], road['position'], road['congestion'])
#
#     for e in roads_dict:
#         entry = roads_dict[e]
#         road = city_roads[entry['name']]
#         if entry['straight'] is not None:
#             road.straight = city_roads[entry['straight']]
#         if entry['left'] is not None:
#             road.left = city_roads[entry['left']]
#         if entry['right'] is not None:
#             road.right = city_roads[entry['right']]
#
#     for road in city_roads:
#         print(city_roads[road].to_a_string())
#
#
# test_build_roads_init(entire_city)
#
# city_roads.create_city(entire_city)
# path, total_running_cost = a_star_search(city_roads.city_roads["Downey Memorial Way E1"], city_roads.city_roads["Massive Road W1"])
# counter = 0
# for p in path:
#     counter += 1
#     print("path: ", counter, p)
