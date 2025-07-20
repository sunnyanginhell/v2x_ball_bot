import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 패키지의 공유 디렉토리 경로 가져오기
    v2x_ball_bot_share_dir = get_package_share_directory('v2x_ball_bot')

    # 각 노드에 대한 파라미터 파일 경로 설정
    ball_detector_params = os.path.join(v2x_ball_bot_share_dir, 'config', 'ball_detector.yaml')
    motion_controller_params = os.path.join(v2x_ball_bot_share_dir, 'config', 'motion_controller.yaml')
    
    # 각 노드를 Node 클래스로 선언
    ball_detector_node = Node(
        package='v2x_ball_bot',
        executable='ball_detector_node',
        name='ball_detector_node',
        parameters=[ball_detector_params],
        output='screen'
    )

    trajectory_predictor_node = Node(
        package='v2x_ball_bot',
        executable='trajectory_predictor_node',
        name='trajectory_predictor_node',
        output='screen'
    )

    path_planner_node = Node(
        package='v2x_ball_bot',
        executable='path_planner_node',
        name='path_planner_node',
        output='screen'
    )

    motion_controller_node = Node(
        package='v2x_ball_bot',
        executable='motion_controller_node',
        name='motion_controller_node',
        parameters=[motion_controller_params],
        output='screen'
    )

    obstacle_avoidance_node = Node(
        package='v2x_ball_bot',
        executable='obstacle_avoidance_node',
        name='obstacle_avoidance_node',
        output='screen'
    )

    ball_pickup_node = Node(
        package='v2x_ball_bot',
        executable='ball_pickup_node',
        name='ball_pickup_node',
        output='screen'
    )

    # LaunchDescription 객체에 실행할 노드들을 추가하여 반환
    return LaunchDescription([
        ball_detector_node,
        trajectory_predictor_node,
        path_planner_node,
        motion_controller_node,
        obstacle_avoidance_node,
        ball_pickup_node
    ])

