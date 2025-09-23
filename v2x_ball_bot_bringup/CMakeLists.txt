cmake_minimum_required(VERSION 3.8)
project(v2x_ball_bot_bringup)

find_package(ament_cmake REQUIRED)

# launch / config / worlds / (있으면) models 설치
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(DIRECTORY config DESTINATION share/${PROJECT_NAME})
install(DIRECTORY maps DESTINATION share/${PROJECT_NAME})

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/models")
  install(DIRECTORY models DESTINATION share/${PROJECT_NAME})
endif()

ament_package()
