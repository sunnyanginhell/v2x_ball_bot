<div align="center">

# V2X Ball Bot

ROS 2 Humble 기반 자율 공 탐지·추적·수거 로봇 프로젝트

![ROS2](https://img.shields.io/badge/ROS%202-Humble-22314E?logo=ros&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?logo=ubuntu&logoColor=white)
![License](https://img.shields.io/badge/License-Apache--2.0-green)

</div>

## 프로젝트 소개

V2X Ball Bot은 RGB-D 카메라와 LiDAR를 사용해 공을 인식하고, 로봇 기준 좌표로 변환한 뒤 공을 따라가 수거 동작까지 수행하는 ROS 2 로봇 시스템입니다. Orbbec depth camera, RPLiDAR, YOLO 기반 공 탐지 모델, Rosmaster 모터 제어, OpenCR 기반 그리퍼 제어를 하나의 워크스페이스에서 운용할 수 있도록 구성되어 있습니다.

이 프로젝트는 실내 주행 환경에서 다음 흐름을 목표로 합니다.

1. Orbbec RGB-D 카메라로 컬러/깊이 영상을 수집합니다.
2. YOLO 모델로 공 후보를 탐지하고 depth 값을 이용해 3D 좌표로 변환합니다.
3. 선택된 공 좌표를 기반으로 로봇이 접근합니다.
4. LiDAR 전방 장애물 감지 결과에 따라 주행을 정지하거나 재개합니다.
5. 목표 거리에 도달하면 OpenCR 그리퍼와 Rosmaster 주행 제어로 수거 시퀀스를 수행합니다.

## 주요 기능

| 기능 | 설명 |
| --- | --- |
| 공 탐지 | RGB 이미지에서 YOLO 모델(`new_ball_detector.pt`)로 공 후보 검출 |
| Depth 좌표화 | RGB-D 동기화와 카메라 내부 파라미터를 이용해 공 위치를 로봇 기준 좌표로 변환 |
| 공 추적 주행 | `/selected_ball` 토픽을 받아 목표 거리까지 선속도/각속도 제어 |
| 수거 시퀀스 | `/pickup_command` 수신 후 그리퍼 하강, 후진, 그리퍼 상승, 완료 신호 발행 |
| 장애물 감지 | LiDAR `/scan` 기반 전방 장애물 감지 및 `/dynamic_obstacle_detect` 발행 |
| 지도/시각화 | SLAM Toolbox, Nav2 map server, RViz2 시각화 launch 제공 |
| Docker 운용 | ROS 2 Humble 개발 컨테이너 기준 실행 명령 정리 |

## 시스템 구성

```mermaid
flowchart LR
    A[Orbbec RGB-D Camera] --> B[ball_perception_node]
    B --> C[/selected_ball]
    C --> D[ball_follower_node]
    E[RPLiDAR /scan] --> F[obstacle_detection_node]
    F --> D
    D --> G[Rosmaster Motor Control]
    D --> H[/pickup_command]
    H --> I[ball_pickup_node]
    I --> J[OpenCR Gripper]
    I --> K[/pickup_complete]
    K --> D
```

## 패키지 구조

```text
.
├── v2x_ball_bot_bringup/        # launch, map, Nav2/SLAM/RViz 설정
├── v2x_ball_bot_control/        # 공 탐지, 추적 주행, 수거, 장애물 감지 노드
├── v2x_ball_bot_description/    # URDF/Xacro, 로봇 및 센서 mesh
├── v2x_ball_bot_msgs/           # Ball, BallArray 등 커스텀 메시지
├── OrbbecSDK_ROS2/              # Orbbec RGB-D 카메라 ROS 2 패키지
├── rplidar_ros/                 # RPLiDAR ROS 2 드라이버
└── README.md
```

## 주요 노드와 토픽

| 노드 | 입력 | 출력 | 역할 |
| --- | --- | --- | --- |
| `ball_perception_node` | `/color/image_raw`, `/depth/image_raw`, `/color/camera_info` | `/selected_ball`, `/debug/ball_detection` | 공 탐지 및 좌표 변환 |
| `ball_follower_node` | `/selected_ball`, `/safety/estop`, `/dynamic_obstacle_detect`, `/pickup_complete` | `/cmd_vel_debug`, `/pickup_command` | 공 접근 주행 및 수거 트리거 |
| `ball_pickup_node` | `/pickup_command` | `/pickup_complete` | 그리퍼와 후진 수거 시퀀스 |
| `obstacle_detection_node` | `/scan` | `/dynamic_obstacle_detect` | 전방 장애물 감지 |
| `motor_driver_node` | `/cmd_vel_out` | `/left_wheel/vel`, `/right_wheel/vel` 또는 serial | 차동 구동 모터 명령 변환 |

## 실행 환경

- Ubuntu 22.04
- ROS 2 Humble
- Python 3.x
- Docker 기반 ROS 2 개발 환경
- Orbbec depth camera
- RPLiDAR A1 계열
- Rosmaster 기반 모바일 베이스
- OpenCR 기반 그리퍼 제어 보드

Python 패키지는 환경에 따라 별도 설치가 필요할 수 있습니다.

```bash
pip install ultralytics opencv-python pyserial numpy
```

## Docker 접속

```bash
sudo docker start -ai main_container
docker exec -it main_container bash
```

RViz2처럼 GUI를 실행해야 하는 경우 호스트에서 X 권한을 열고 컨테이너에 접속합니다.

```bash
xhost +local:docker
docker exec -it ros2_humble_dev_usb bash
export DISPLAY=:0
rviz2
```

## 빌드

### 전체 클린 빌드

```bash
cd ~/ros2_ws
rm -rf build/ install/ log/
colcon build --symlink-install
source install/setup.bash
```

### bringup/control만 클린 빌드

```bash
cd ~/ros2_ws
rm -rf build/v2x_ball_bot_control install/v2x_ball_bot_control log/v2x_ball_bot_control
rm -rf build/v2x_ball_bot_bringup install/v2x_ball_bot_bringup log/v2x_ball_bot_bringup

colcon build --symlink-install --packages-select \
  v2x_ball_bot_control \
  v2x_ball_bot_bringup

source install/setup.bash
```

## 실행 가이드

### 1. Depth camera 실행

Launch 파일을 사용하는 방법입니다.

```bash
ros2 launch v2x_ball_bot_bringup orbbec_camera.launch.py
```

직접 노드를 실행하려면 아래 명령을 사용할 수 있습니다.

```bash
ros2 run orbbec_camera orbbec_camera_node \
  --ros-args \
  -p enable_color:=true \
  -p enable_depth:=true \
  -p enable_align_depth_to_color:=true \
  -p color_width:=640 \
  -p color_height:=480 \
  -p color_fps:=30 \
  -p depth_width:=640 \
  -p depth_height:=480 \
  -p depth_fps:=30 \
  -p depth_format:=Y12
```

### 2. 공 인식 노드 실행

```bash
colcon build --packages-select v2x_ball_bot_control
source install/setup.bash

ros2 launch v2x_ball_bot_bringup ball_perception.launch.py
```

디버그 이미지 확인:

```bash
ros2 topic echo /selected_ball
ros2 topic echo /debug/ball_detection
```

### 3. LiDAR 실행

```bash
ros2 launch rplidar_ros rplidar_a1_launch.py
```

또는 bringup launch를 사용해 LiDAR, TF, SLAM, robot state publisher를 함께 실행할 수 있습니다.

```bash
docker exec -it main_container bash -lc '
source /opt/ros/humble/setup.bash && source /root/ros2_ws/install/setup.bash &&
ros2 launch v2x_ball_bot_bringup bringup_min.launch.py \
  lidar_port:=/dev/ttyUSB0 lidar_baud:=115200 lidar_scan_mode:=Standard'
```

### 4. 장애물 감지 실행

```bash
ros2 run v2x_ball_bot_control obstacle_detection_node
```

결과 토픽 확인:

```bash
ros2 topic echo /dynamic_obstacle_detect
```

### 5. 공 추적 주행 실행

USB 포트는 실제 장치에 맞게 변경합니다.

```bash
ros2 run v2x_ball_bot_control ball_follower_node \
  --ros-args -p serial_port:=/dev/ttyUSB1
```

주요 파라미터:

| 파라미터 | 기본값 | 설명 |
| --- | --- | --- |
| `ball_topic` | `/selected_ball` | 추적할 공 좌표 토픽 |
| `target_dist_m` | `0.3` | 공과 유지할 목표 거리 |
| `v_max` | `1.0` | 최대 선속도 |
| `w_max` | `1.0` | 최대 각속도 |
| `ball_timeout_sec` | `1.0` | 공 좌표 timeout |
| `serial_port` | `/dev/ttyUSB1` | Rosmaster 연결 포트 |

### 6. 공 수거 노드 실행

```bash
ros2 run v2x_ball_bot_control ball_pickup_node \
  --ros-args -p serial_port:=/dev/ttyUSB1 -p opencr_port:=/dev/ttyACM0
```

수거 노드는 `/pickup_command`가 `true`일 때 다음 순서로 동작합니다.

1. OpenCR에 그리퍼 하강 명령 전송
2. Rosmaster로 약 1m 후진
3. OpenCR에 그리퍼 상승 명령 전송
4. `/pickup_complete` 발행

### 7. 모터 드라이버 단독 실행

토픽 백엔드:

```bash
ros2 run v2x_ball_bot_control motor_driver_node \
  --ros-args -p cmd_topic:=/cmd_vel_out \
             -p wheel_radius:=0.05 -p wheel_base:=0.30 \
             -p backend:=topic \
             -p left_topic:=/left_wheel/vel -p right_topic:=/right_wheel/vel
```

Serial 백엔드:

```bash
ros2 run v2x_ball_bot_control motor_driver_node \
  --ros-args -p backend:=serial \
             -p serial_port:=/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0 \
             -p serial_baud:=115200
```

## 지도와 RViz2

### 고정 맵 표시

```bash
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom
ros2 launch v2x_ball_bot_bringup display_map.launch.py
```

RViz2에서 Map display를 추가한 뒤 topic을 `/map`으로 설정하고 QoS를 아래처럼 변경합니다.

- Reliability: `Reliable`
- Durability: `Transient Local`

### 맵 파일 직접 지정

```bash
ros2 launch v2x_ball_bot_bringup display_map.launch.py \
  map:=/absolute/path/to/map.yaml
```

또는 환경변수로 지정할 수 있습니다.

```bash
export MAP_YAML=/absolute/path/to/map.yaml
ros2 launch v2x_ball_bot_bringup display_map.launch.py
```

## 자주 쓰는 점검 명령

```bash
ros2 node list
ros2 topic list
ros2 topic echo /selected_ball
ros2 topic echo /dynamic_obstacle_detect
ros2 topic hz /color/image_raw
ros2 topic hz /depth/image_raw
ros2 run tf2_tools view_frames
```

## 권한 문제 해결

파일 소유권 문제로 노드 실행이 막힐 때:

```bash
sudo chown ss802:ss802 /home/ss802/ros2_ws/src/v2x_ball_bot_control/v2x_ball_bot_control/ball_pickup_node.py
sudo chown -R ss802:ss802 /home/ss802/ros2_ws/src/v2x_ball_bot_control
```

시리얼 장치 접근 권한이 없을 때:

```bash
sudo usermod -aG dialout $USER
```

설정 후 로그아웃/로그인 또는 컨테이너 재시작이 필요할 수 있습니다.

## 참고 자료

- Drive 자료: https://drive.google.com/drive/folders/1AKHB_Y0bQoje9KC5DslliCRysFL5NmXu?usp=sharing
- ROS 2 Humble: https://docs.ros.org/en/humble/
- OrbbecSDK ROS2: https://github.com/orbbec/OrbbecSDK_ROS2
- Slamtec RPLiDAR ROS: https://github.com/Slamtec/rplidar_ros

## 라이선스

이 프로젝트의 ROS 2 패키지는 `Apache-2.0` 라이선스를 기준으로 작성되어 있습니다. 외부 포함 패키지와 SDK는 각 프로젝트의 라이선스를 따릅니다.
