from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    map_yaml = "/home/yuha/V2X-ball-bot/v2x_ball_bot_bringup/maps/map.yaml"
    return LaunchDescription([
        Node(
            package="nav2_map_server",
            executable="map_server",
            name="map_server",
            parameters=[{"yaml_filename": map_yaml}],
        ),
        Node(
            package="nav2_lifecycle_manager",
            executable="lifecycle_manager",
            name="lifecycle_manager_map",
            parameters=[{
                "use_sim_time": False,
                "autostart": True,
                "node_names": ["map_server"]
            }],
        ),
    ])
