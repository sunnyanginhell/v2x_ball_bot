from setuptools import setup
from glob import glob

package_name = 'v2x_ball_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],  # OK
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sunnyangee',
    maintainer_email='none@example.com',
    description='ROS 2 node package for V2X communication bot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ball_node = v2x_ball_bot.ball_node:main',
        ],
    },
)
