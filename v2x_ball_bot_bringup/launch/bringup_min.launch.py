from launch import LaunchDescription
from launch_ros.actions import Node
import os
import xacro
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # === 로봇 모델 (xacro → urdf 변환) ===
    xacro_file = os.path.join(
        get_package_share_directory('v2x_ball_bot_description'),
        'urdf',
        'yahboomcar_X3.urdf.xacro'
    )
    robot_description_config = xacro.process_file(xacro_file).toxml()

    # === LiDAR ===
    rplidar = Node(
        package='rplidar_ros',
        executable='rplidar_composition',
        name='rplidar',
        parameters=[{
            'channel_type': 'serial',
            'serial_port': '/dev/ttyUSB0',   # 필요 시 /dev/ttyUSB1
            'serial_baudrate': 115200,       # Express 모델은 256000
            'frame_id': 'laser',
            'angle_compensate': True,
            'scan_mode': 'Standard',
        }],
    )

    # === LiDAR → base_link TF ===
    tf_laser = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0','0','0.12','0','0','0','base_link','laser']  # 실제 높이 0.12m
    )

    # === 임시 map → odom TF ===
    tf_map_odom = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_map_to_odom',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
        output='screen'
    )

    # === 임시 odom → base_link TF ===
    tf_odom = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0','0','0','0','0','0','odom','base_link']
    )

    # === Camera → base_link TF ===
    tf_camera = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_base_to_camera',
        arguments=['0', '0', '0.1', '0', '0', '0', 'base_link', 'orbbec_camera_link'],  # 카메라 높이 0.1m
        output='screen'
    )

    # === SLAM Toolbox (async 모드로 통일) ===
    slam = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[{
            'odom_frame': 'odom',
            'map_frame': 'map',
            'base_frame': 'base_link',
            'scan_topic': '/scan',
            'publish_tf': True,
            'resolution': 0.05,
            'mode': 'mapping',
        }],
        output='screen'
    )

    # === 맵 서버 추가 ===
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'yaml_filename': os.path.join(
                get_package_share_directory('v2x_ball_bot_bringup'),
                'maps', 'map.yaml'
            )
        }]
    )

    # === Robot State Publisher (URDF → TF, 로봇 모델 표시) ===
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'use_sim_time': False,
            'robot_description': robot_description_config
        }],
        output='screen'
    )

    return LaunchDescription([
        rplidar,
        tf_laser,
        tf_odom,
        tf_camera,
        slam,
        map_server,
        robot_state_publisher
    ])
