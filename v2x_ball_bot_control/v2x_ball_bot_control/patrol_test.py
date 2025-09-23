#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from tf2_ros import Buffer, TransformListener, TransformException
from tf_transformations import euler_from_quaternion
import math
import time

# Rosmaster 클래스를 임포트합니다.
from v2x_ball_bot_control.rosmaster import Rosmaster

class MapBasedPatrolNode(Node):
    def __init__(self):
        super().__init__('map_based_patrol_node')
        self.get_logger().info('맵 기반 순찰 노드 초기화')

        # === 1. 파라미터 선언 ===
        self.serial_port = self.declare_parameter('serial_port', '/dev/ttyUSB1').value
        self.car_type = self.declare_parameter('car_type', 1).value
        self.P_GAIN_ANGULAR = self.declare_parameter('p_gain_angular', 1.5).value
        self.P_GAIN_LINEAR = self.declare_parameter('p_gain_linear', 0.4).value
        self.GOAL_TOLERANCE_DIST = self.declare_parameter('goal_tolerance_dist', 0.15).value
        self.GOAL_TOLERANCE_ANGLE = self.declare_parameter('goal_tolerance_angle', 0.1).value
        self.MAP_MARGIN = self.declare_parameter('map_margin_m', 0.25).value # 벽에서 떨어질 거리

        # === 2. 상태 변수 초기화 ===
        self.is_map_received = False
        self.goal_points = []
        self.current_goal_index = -1  # -1은 아직 순찰 시작 전임을 의미

        # === 3. Rosmaster 및 TF 리스너 초기화 ===
        self.bot = None
        try:
            self.bot = Rosmaster(car_type=self.car_type, com=self.serial_port)
            self.get_logger().info(f"Rosmaster 연결 성공: {self.serial_port}")
        except Exception as e:
            self.get_logger().error(f"Rosmaster 연결 실패: {e}")
            rclpy.shutdown()
            return

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # === 4. ROS 2 서브스크라이버 및 타이머 설정 ===
        self.map_subscriber = self.create_subscription(
            OccupancyGrid, '/map', self.map_callback, 10) # qos는 republisher와 맞춤
        
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info("초기화 완료. /map 토픽을 기다립니다...")

    def map_callback(self, msg: OccupancyGrid):
        if self.is_map_received:
            return # 맵 정보는 한 번만 처리

        self.get_logger().info("맵 정보 수신 완료! 목표 지점을 계산합니다.")
        self.is_map_received = True

        # 맵 정보에서 실제 세계의 크기와 원점을 추출
        width_m = msg.info.width * msg.info.resolution
        height_m = msg.info.height * msg.info.resolution
        origin_x = msg.info.origin.position.x
        origin_y = msg.info.origin.position.y

        # 맵의 네 꼭짓점 좌표를 계산 (여유 공간 적용)
        margin = self.MAP_MARGIN
        self.goal_points = [
            {'x': origin_x + margin,     'y': origin_y + margin},
            {'x': origin_x + width_m - margin, 'y': origin_y + margin},
            {'x': origin_x + width_m - margin, 'y': origin_y + height_m - margin},
            {'x': origin_x + margin,     'y': origin_y + height_m - margin}
        ]
        
        self.get_logger().info(f"계산된 목표 지점: {self.goal_points}")
        self.current_goal_index = 0 # 첫 번째 목표부터 순찰 시작
        self.get_logger().info("순찰을 시작합니다!")


    def control_loop(self):
        if not self.is_map_received or self.current_goal_index == -1:
            # 아직 맵을 받지 못했으면 아무것도 하지 않음
            return

        # TF를 이용한 현재 위치 파악
        try:
            t = self.tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
        except TransformException as ex:
            self.get_logger().warn(f'TF 변환 실패: {ex}', throttle_duration_sec=1.0)
            self.send_motor_command(0.0, 0.0, 0.0)
            return
            
        robot_x = t.transform.translation.x
        robot_y = t.transform.translation.y
        q = t.transform.rotation
        _, _, robot_yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])

        # 목표 지점까지의 거리 및 각도 오차 계산
        target_goal = self.goal_points[self.current_goal_index]
        dist_error = math.sqrt((target_goal['x'] - robot_x)**2 + (target_goal['y'] - robot_y)**2)
        angle_to_goal = math.atan2(target_goal['y'] - robot_y, target_goal['x'] - robot_x)
        angle_error = angle_to_goal - robot_yaw
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

        # 목표 도착 여부 확인
        if dist_error < self.GOAL_TOLERANCE_DIST:
            self.get_logger().info(f"목표 지점 {self.current_goal_index + 1} 도착!")
            self.send_motor_command(0.0, 0.0, 0.0)
            self.current_goal_index = (self.current_goal_index + 1) % len(self.goal_points)
            self.get_logger().info(f"다음 목표({self.current_goal_index + 1})로 이동합니다...")
            time.sleep(2.0) # 다음 목표로 가기 전 2초 대기
            return

        # 제어 명령(vx, wz) 생성 및 전송
        vx, wz = 0.0, 0.0
        if abs(angle_error) > self.GOAL_TOLERANCE_ANGLE:
            wz = self.P_GAIN_ANGULAR * angle_error
        else:
            vx = self.P_GAIN_LINEAR * dist_error
            wz = self.P_GAIN_ANGULAR * angle_error
        
        self.send_motor_command(vx, 0.0, wz)

    def send_motor_command(self, vx, vy, wz):
        if self.bot is not None:
            self.bot.set_car_motion(vx, vy, wz)

    def destroy_node(self):
        self.get_logger().info("노드 종료. 로봇을 정지합니다.")
        if self.bot is not None:
            self.bot.set_car_motion(0.0, 0.0, 0.0)
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = MapBasedPatrolNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()