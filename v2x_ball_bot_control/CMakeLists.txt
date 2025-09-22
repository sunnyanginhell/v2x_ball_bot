cmake_minimum_required(VERSION 3.5)
project(v2x_ball_bot_control)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

# Python 패키지 설치 (import 편의성)
ament_python_install_package(v2x_ball_bot_control)

# =========================
# Nodes 설치
# =========================


# ball_perception_node 설치 
install(PROGRAMS
  v2x_ball_bot_control/ball_perception_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ball_perception_node
)

# ball_follower_node 설치 
install(PROGRAMS
  v2x_ball_bot_control/ball_follower_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ball_follower_node
)

# ball_pickup_node 설치
install(PROGRAMS
  v2x_ball_bot_control/ball_pickup_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ball_pickup_node
)

# obstacle_detection_node 설치
install(PROGRAMS
  v2x_ball_bot_control/obstacle_detection_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME obstacle_detection_node
)

# odom_tf_pub 설치
install(PROGRAMS
  v2x_ball_bot_control/odom_tf_pub.py
  DESTINATION lib/${PROJECT_NAME}
  PERMISSIONS OWNER_EXECUTE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ
)

# ball_goal_transform_node 설치
install(PROGRAMS
  v2x_ball_bot_control/map_transform_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME map_transform_node
)

# ✅ YOLO 모델 파일 함께 설치
install(FILES
  v2x_ball_bot_control/new_ball_detector.pt
  DESTINATION lib/${PROJECT_NAME}
)

# ✅ scan_manager 설치
# install(PROGRAMS
#  v2x_ball_bot_control/scan_manager.py
#  DESTINATION lib/${PROJECT_NAME}
#  RENAME scan_manager
#  PERMISSIONS OWNER_EXECUTE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ
# )

# ✅ court_manager 설치
install(PROGRAMS
  v2x_ball_bot_control/court_manager.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME court_manager
  PERMISSIONS OWNER_EXECUTE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ
)

# ⚠️ 현재 twist_mux.yaml 없음 → 주석 처리
# install(FILES
#   config/twist_mux.yaml
#   DESTINATION share/${PROJECT_NAME}/config
# )

# (선택) 파라미터 YAML share에 설치
# install(FILES
#  config/scan_manager.yaml
#  config/court_manager.yaml
#  DESTINATION share/${PROJECT_NAME}/config
# )

# launch 디렉토리 설치
# install(DIRECTORY
#  launch
#  DESTINATION share/${PROJECT_NAME}
# )

ament_package()
