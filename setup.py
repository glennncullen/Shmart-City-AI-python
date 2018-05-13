import sys

sys.path.insert(0, 'app')

from setuptools import setup

setup(
    name='Shmart City AI',
    packages=[
        'app',
        'app.communication',
        'app.search.a_star',
        'app.communication.pub_nub',
        'app.city.street_node',
        'app.city.city_map'
    ],
    version="0.0",
    author='Glenn Cullen',
    description='AI for Shmart City',
    install_requires=[
        'pubnub>=4.0.13',
        'AWSIoTPythonSDK'
    ]
)