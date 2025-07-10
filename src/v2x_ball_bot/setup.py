from setuptools import setup
from glob import glob

package_name = 'v2x_ball_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],  # 반드시 패키지 디렉토리명과 동일하게
    data_files=[
        ('share/ament_index/resource_index/packages',
            [f'resource/{package_name}']),
        (f'share/{package_name}', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sunnyangee',
    maintainer_email='sunnyangee@example.com',
    description='V2X ROS2 bot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ball_node = v2x_ball_bot.ball_node:main',
        ],
    },
)
