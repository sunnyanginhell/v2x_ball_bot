from setuptools import find_packages
from setuptools import setup

setup(
    name='v2x_ball_bot_control',
    version='0.0.0',
    packages=find_packages(
        include=('v2x_ball_bot_control', 'v2x_ball_bot_control.*')),
)
