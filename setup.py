import sys

sys.path.insert(0, 'app')

from setuptools import setup

setup(
    name='Shmart City AI',
    packages=[
        'app',
        'app.mqtt'
    ],
    version="0.0",
    author='Glenn Cullen',
    description='AI for Shmart City',
    install_requires=[
        'numpy',
    ]
)
