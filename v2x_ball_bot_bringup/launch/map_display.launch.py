#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 패키지 경로 가져오기
    pkg_share = get_package_share_directory('v2x_ball_bot_bringup')
    rviz_config = os.path.join(pkg_share, 'config', 'ball_perception.rviz')
    
    # bringup_min 실행 (LiDAR, SLAM, 맵 서버 포함)
    bringup_min = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(pkg_share, 'launch', 'bringup_min.launch.py')
        ])
    )
    
    # RViz 실행
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )
    
    return LaunchDescription([
        bringup_min,
        rviz_node
    ])
