#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from v2x_ball_bot_msgs.msg import BallArray
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
import math
import time
from typing import Optional

from v2x_ball_bot_control.rosmaster import Rosmaster

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

class BallFollowerNode(Node):
    def __init__(self):
        super().__init__('ball_follower_node')
        self.get_logger().info('공 추적 제어 노드 초기화 시작')

        # (파라미터 선언 부분은 기존과 동일)
        self.ball_topic = self.declare_parameter('ball_topic', '/balls').value
        self.estop_topic = self.declare_parameter('estop_topic', '/safety/estop').value
        self.k_linear = self.declare_parameter('k_linear', 0.4).value
        self.k_angular = self.declare_parameter('k_angular', 1.0).value
        self.target_dist = self.declare_parameter('target_dist_m', 0.1).value
        self.max_linear_speed = self.declare_parameter('v_max', 1.0).value
        self.max_angular_speed = self.declare_parameter('w_max', 1.0).value
        self.accel_linear = self.declare_parameter('accel_v', 0.3).value
        self.accel_angular = self.declare_parameter('accel_w', 0.1).value
        self.stop_margin = self.declare_parameter('stop_margin_m', 0.4).value
        self.deadband_yaw_deg = self.declare_parameter('deadband_yaw_deg', 5.0).value
        self.ball_timeout = self.declare_parameter('ball_timeout_sec', 1.0).value
        self.y_scale_correction = self.declare_parameter('y_scale_correction', 0.5).value
        self.serial_port = self.declare_parameter('serial_port', '/dev/ttyUSB1').value
        self.car_type = self.declare_parameter('car_type', 1).value
        self.use_depth_priority = self.declare_parameter('use_depth_priority', True).value

        # (상태 변수, Rosmaster 초기화 부분은 기존과 동일)
        self.estop = False
        self.last_ball_xyz: Optional[tuple[float, float, float]] = None
        self.last_stamp_sec: float = 0.0
        self.is_following = True
        self.current_vx = 0.0
        self.current_wz = 0.0
        self.bot = None
        try:
            self.bot = Rosmaster(car_type=self.car_type, com=self.serial_port)
            self.bot.create_receive_threading()
            time.sleep(0.1)
            self.bot.set_car_type(self.car_type)
            self.get_logger().info(f"Rosmaster 시리얼 포트 연결 성공: {self.serial_port}")
        except Exception as e:
            self.get_logger().error(f"Rosmaster 시리얼 포트 연결 실패: {e}")

        # ROS Publisher & Subscriber
        self.sub_ball = self.create_subscription(BallArray, self.ball_topic, self.ball_callback, 10)
        self.sub_estop = self.create_subscription(Bool, self.estop_topic, self.estop_callback, 10)
        self.pub_debug = self.create_publisher(Twist, '/cmd_vel_debug', 10)
        self.pub_pickup = self.create_publisher(Bool, '/pickup_command', 10)
        # ✅ Pickup 노드로부터 작업 완료 신호를 받을 서브스크라이버 추가
        self.sub_complete = self.create_subscription(
            Bool, '/pickup_complete', self.pickup_complete_callback, 10)

        # 제어 루프 타이머
        self.dt = 0.05
        self.timer = self.create_timer(self.dt, self.control_loop)
        self.get_logger().info("초기화 완료. 공 추적을 시작합니다.")

    # ✅ Pickup 완료 신호를 처리할 콜백 함수 추가
    def pickup_complete_callback(self, msg: Bool):
        if msg.data:
            self.get_logger().info("Pickup 완료 신호 수신! 다시 공 추적을 시작합니다.")
            self.is_following = True # 추적 상태를 다시 활성화
            self.last_ball_xyz = None # 이전 공의 위치 정보를 초기화
            self.last_stamp_sec = 0.0

    def ball_callback(self, msg: BallArray):
        if msg.balls and self.is_following:
            ball = msg.balls[0]
            self.last_ball_xyz = (ball.x, ball.y, ball.z)
            self.last_stamp_sec = self.get_clock().now().nanoseconds * 1e-9

    def estop_callback(self, msg: Bool):
        self.estop = msg.data
        if self.estop: self.get_logger().warn("비상 정지(E-stop) 신호 수신!")

    def control_loop(self):
        # (이하 control_loop 및 다른 함수들은 이전 버전과 동일)
        if not self.is_following:
            if self.current_vx != 0.0 or self.current_wz != 0.0:
                self.current_vx = self.slew(self.current_vx, 0.0, self.accel_linear * self.dt)
                self.current_wz = self.slew(self.current_wz, 0.0, self.accel_angular * self.dt)
                self.send_motor_command(self.current_vx, 0.0, self.current_wz)
            return

        if self.estop or self.is_timed_out() or self.last_ball_xyz is None:
            if self.is_following:
                self.get_logger().info('추적 활성화 상태 : 공 좌표를 기다리는중 ....')
            target_vx, target_wz = 0.0, 0.0
        else:
            x, y, z = self.last_ball_xyz
            y_corrected = y * self.y_scale_correction
            distance = z if self.use_depth_priority and z > 0.0 else math.hypot(x, y_corrected)
            angle = math.atan2(y_corrected, x)

            is_goal_reached = (distance < self.target_dist + self.stop_margin) and \
                                (abs(angle) < math.radians(self.deadband_yaw_deg))

            if is_goal_reached:
                self.get_logger().info("목표 지점 도달! Pickup 노드에 수거 명령 전송.")
                target_vx, target_wz = 0.0, 0.0

                pickup_msg = Bool()
                pickup_msg.data = True
                self.pub_pickup.publish(pickup_msg)
                self.is_following = False
            else:
                error_dist = distance - self.target_dist
                target_vx = self.k_linear * error_dist
                target_wz = self.k_angular * angle
                target_vx = clamp(target_vx, 0.0, self.max_linear_speed)
                target_wz = clamp(target_wz, -self.max_angular_speed, self.max_angular_speed)

        self.current_vx = self.slew(self.current_vx, target_vx, self.accel_linear * self.dt)
        self.current_wz = self.slew(self.current_wz, target_wz, self.accel_angular * self.dt)
        self.send_motor_command(self.current_vx, 0.0, self.current_wz)

    def is_timed_out(self) -> bool:
        if self.last_stamp_sec == 0.0: return True
        return (self.get_clock().now().nanoseconds * 1e-9 - self.last_stamp_sec) > self.ball_timeout

    def slew(self, current_val, target_val, step):
        if target_val > current_val + step: return current_val + step
        if target_val < current_val - step: return current_val - step
        return target_val

    def send_motor_command(self, vx, vy, wz):
        debug_twist = Twist()
        debug_twist.linear.x = vx
        debug_twist.angular.z = wz
        self.pub_debug.publish(debug_twist)
        if self.bot is not None:
            self.bot.set_car_motion(vx, vy, wz)

    def destroy_node(self):
        self.get_logger().info("노드 종료. 로봇을 정지합니다.")
        if self.bot is not None:
            self.bot.set_car_motion(0.0, 0.0, 0.0)
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = BallFollowerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
