import rclpy
from rclpy.node import Node
from v2x_ball_bot_msgs.msg import Ball
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

        #ROS2 파라미터 선언(launch 파일에서 쉽게 값을 변경하기 위함)
        self.ball_topic = self.declare_parameter('ball_topic','/ball').value
        self.estop_topic = self.declare_parameter('estop_topic', '/safety/estop').value

        #P 제어 (핵심 튜닝값)
        self.k_linear = self.declare_parameter('k_linear', 0.8).value #전진 속도 비례
        self.k_angular = self.declare_parameter('k_angular', 1.5).value #회전 속도 비례

        #목표 및 속도 제한
        self.target_dist = self.declare_parameter('target_dist_m', 0.3).value #로봇과 공 사이의 목표 거리
        self.max_linear_speed = self.declare_parameter('v_max', 0.3).value #최대 전진 속도(m/s)
        self.max_angular_speed = self.declare_parameter('w_max', 0.8).value #최대 회전 속도(rad/s)

        #가감속 제한(Slew Rate)
        self.accel_linear = self.declare_parameter('accel_v', 0.8).value #전진 가속도
        self.accel_angular = self.declare_parameter('accel_w', 1.5).value #회전 가속도

        #정지 조건(데드밴드)
        self.stop_margin = self.declare_parameter('stop_margin_m', 0.05).value #목표 거리 허용 오차
        self.deadband_yaw_deg = self.declare_parameter('deadband_yaw_deg', 5.0).value #목표 각도 허용 오차

        #타임 아웃
        self.ball_timeout = self.declare_parameter('ball_timeout_sec', 1.0).value #공 인식 타임아웃(sec)

        #Rosmaster 시리얼 포트 설정
        self.serial_port = self.declare_parameter('serial_port', '/dev/ttyUSB0').value
        self.car_type = self.declare_parameter('car_type', 1).value

        #거리 계산 우선순위 파라미터
        self.use_depth_priority = self.declare_parameter('use_depth_priority', True).value

        #-------------상태 변수---------------
        self.estop = False
        self.last_ball_xy: Optional[tuple[float, float, float]] = None
        self.last_stamp_sec: float = 0.0

        #현재 로봇의 속도 (가감속 제어를 위해 필요함)
        self.current_vx = 0.0
        self.current_vy = 0.0
        self.current_wz = 0.0

        #--------------Rosmaster 초기화--------
        self.bot = None
        try:
            self.bot = Rosmaster(car_type=self.car_type, com=self.serial_port)
            self.bot.create_receive_threading()
            time.sleep(0.1)
            self.bot.set_car_type(self.car_type)
            self.get_logger().info(f"Rosmaster 시리얼 포트 연결 성공: {self.serial_port}")
        except Exception as e:
            self.get_logger().error(f"Rosmaster 시리얼 포트 연결 실패: {e}")

        #-------------Ros Publisher & Subscriber----------------
        self.sub_ball = self.create_subscription(Ball, self.ball_topic, self.ball_callback, 10)
        self.sub_estop = self.create_subscription(Bool, self.estop_topic, self.estop_callback, 10)
        self.pub_debug = self.create_publisher(Twist, '/cmd_vel_debug', 10) #디버깅용 Twist 메시지 발행

        #-------------제어 루프 타이머----------------
        self.dt = 0.05
        self.timer = self.create_timer(self.dt, self.control_loop)
        self.get_logger().info("초기화 완료. 공 추적을 시작합니다.")
    
    def ball_callback(self, msg: Ball):
        self.last_bal_xyz = (msg.x, msg.y, msg.z)
        self.last_stamp_sec = self.get_clock().now().nanoseconds * 1e-9

    def estop_callback(self, msg: Bool):
        self.estop = msg.data
        if self.estop:
            self.get_logger().warn("비상 정지(E-stop) 신호 수신!")

    def control_loop(self):
        #1. 안전 조건 확인(비상정지, 타임아웃, 공 미발견)
        if self.estop or self.is_timed_out() or self.last_ball_xy is None:
            target_vx, target_wz = 0.0, 0.0
        else:
            #2. 목표 속도 계산
            x, y, z= self.last_ball_xyz

            #z값이 유효하고, depth_priority가 켜져있으면 z를 사용
            if self.use_depth_priority and z > 0.0:
                distance = z
                dist_type = "depth(z)"
            else:
                distance = math.hypot(x, y)
                dist_type = "planar(xy)"

            angle = math.atan2(y, x)

            self.get_logger().info(f"거리 계산 방식: {dist_type}", throttle_duration_sec=1)

            #3. 정지 조건 확인(데드밴드)
            is_goal_reached = (distance < self.target_dist + self.stop_margin) and \
                                (abs(angle) < math.radians(self.deadband_yaw_deg))
            
            if is_goal_reached:
                target_vx, target_wz = 0.0, 0.0
            else:
                # P 제어 : 오차에 비례하여 목표 속도 계산
                error_dist = distance - self.target_dist
                target_vx = self.k_linear * error_dist
                target_wz = self.k_angular * angle

                #속도 제한
                target_vx = clamp(target_vx, 0.0, self.max_linear_speed) #후진 방지
                target_wz = clamp(target_wz, -self.max_angular_speed, self.max_angular_speed)
                
        #4. 가감속 제한 적용(Slew Rate)
        self.current_vx = self.slew(self.current_vx, target_vx, self.accel_linear * self.dt)
        self.current_wz = self.slew(self.current_wz, target_wz, self.accel_angular * self.dt)

        #5. 최종 명령 전송
        self.send_motor_command(self.current_vx, 0.0, self.current_wz)

    def is_timed_out(self) -> bool:
        if self.last_stamp_sec == 0.0 : return True

        is_timeout = (self.get_clock().now().nanoseconds * 1e-9 - self.last_stamp_sec) > self.ball_timeout
        if is_timeout:
            self.get_logger().warn(f"공 인식 타임아웃! ({self.ball_timeout}초 초과)", throttle_duration_sec=1)
        return is_timeout
    
    def slew(self, current_val: float, target_val: float, step: float) -> float:
        if target_val > current_val + step:
            return current_val + step
        if target_val < current_val - step:
            return current_val - step
        return target_val
    
    def send_motor_commnad(self, vx:float, vy:float, wz:float):
        debug_twist = Twist()
        debug_twist.linear.x = vx
        debug_twist.angular.z = wz
        self.pub_debug.publish(debug_twist)

        #Rosmaster에 실제 명령 전송
        if self.bot is not None:
            try:
                self.bot.set_car_motion(vx, vy, wz)
            except Exception as e:
                self.get_logger().error(f"Rosmaster 명령 전송 실패: {e}")
    
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
        #종료 시 노드를 안전하게 파괴하기 위함
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()