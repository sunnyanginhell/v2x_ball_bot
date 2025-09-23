from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def pick_map_yaml(user_arg: str):
    # 1) CLI 인자 우선
    if user_arg and os.path.exists(user_arg):
        return user_arg
    # 2) 환경변수 MAP_YAML
    env = os.environ.get("MAP_YAML", "")
    if env and os.path.exists(env):
        return env
    # 3) 소스 트리(개발 중): 사용자가 준 경로
    p_src = "/home/ss802/ros2_ws/src/v2x_ball_bot_bringup/maps/my_map.yaml"
    if os.path.exists(p_src):
        return p_src
    # 4) 설치 트리(install 후)
    pkg_share = get_package_share_directory("v2x_ball_bot_bringup")
    p_install = os.path.join(pkg_share, "maps", "my_map.yaml")
    if os.path.exists(p_install):
        return p_install
    # 5) 마지막 안전장치: 없으면 예외
    raise FileNotFoundError("맵 yaml을 찾지 못했습니다. CLI 인자나 MAP_YAML 환경변수를 지정해주세요.")

def generate_launch_description():
    map_arg = DeclareLaunchArgument(
        "map", default_value="",  # 비워두면 자동탐색
        description="맵 yaml 절대경로(옵션). 비우면 자동탐색합니다."
    )
    map_cfg = LaunchConfiguration("map")

    # pick in Python at launch time
    map_yaml = pick_map_yaml(os.environ.get("LAUNCH_MAP_OVERRIDE","") or "")

    map_server = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[{"yaml_filename": map_yaml}],
    )

    amcl = Node(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        parameters=[{
            "use_sim_time": False,
            "base_frame_id": "base_link",
            "odom_frame_id": "odom",
            "global_frame_id": "map",
            "scan_topic": "/scan",
            "min_particles": 500, "max_particles": 2000,
            "update_min_d": 0.05, "update_min_a": 0.05,
            "resample_interval": 1, "kld_err": 0.05, "kld_z": 0.99,
            "laser_model_type": "likelihood_field",
            "laser_likelihood_max_dist": 2.0,
            "laser_max_range": 8.0, "laser_min_range": 0.1,
            "transform_tolerance": 0.2,
        }],
    )

    lifecycle = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_map",
        output="screen",
        parameters=[{
            "use_sim_time": False,
            "autostart": True,
            "node_names": ["map_server", "amcl"],
        }],
    )

    static_base_to_laser = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_base_to_laser",
        arguments=["0.14","0.0","0.12","0","0","0","base_link","laser"],
        output="screen",
    )

    return LaunchDescription([
        map_arg,
        map_server,
        amcl,
        lifecycle,
        static_base_to_laser,
    ])
