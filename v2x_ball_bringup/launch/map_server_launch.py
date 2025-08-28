#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 패키지 경로 가져오기
    pkg_share = get_package_share_directory('v2x_ball_bot_bringup')
    map_dir = os.path.join(pkg_share, 'maps')
    map_file = os.path.join(map_dir, 'map.yaml')
    
    return LaunchDescription([
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{
                'yaml_filename': map_file
            }]
        )
    ])
