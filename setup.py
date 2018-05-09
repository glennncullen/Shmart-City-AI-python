import sys

sys.path.insert(0, 'app')

from setuptools import setup

setup(
    name='Shmart City AI',
    packages=[
        'app',
        'app.communication'
    ],
    version="0.0",
    author='Glenn Cullen',
    description='AI for Shmart City',
    install_requires=[
        'numpy',
        'pubnub>=4.0.13'
    ]
)
