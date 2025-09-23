#!/usr/bin/env python3
import math
import time
import signal
import atexit

import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from tf2_ros import Buffer, TransformListener, TransformException
from tf_transformations import euler_from_quaternion

# Rosmaster (실로봇 모션 명령)
from v2x_ball_bot_control.rosmaster import Rosmaster


class MapBasedPatrolNode(Node):
    def __init__(self):
        super().__init__('map_based_patrol_node')
        self.get_logger().info('맵 기반 순찰 노드 초기화')

        # === 1) 파라미터 ===
        self.serial_port = self.declare_parameter('serial_port', '/dev/ttyUSB1').value
        self.car_type = self.declare_parameter('car_type', 1).value

        self.P_GAIN_ANGULAR = self.declare_parameter('p_gain_angular', 1.5).value
        self.P_GAIN_LINEAR  = self.declare_parameter('p_gain_linear', 0.4).value
        self.GOAL_TOLERANCE_DIST  = self.declare_parameter('goal_tolerance_dist', 0.15).value
        self.GOAL_TOLERANCE_ANGLE = self.declare_parameter('goal_tolerance_angle', 0.1).value
        self.MAP_MARGIN = self.declare_parameter('map_margin_m', 0.25).value

        # 안전 파라미터
        self.V_MAX = self.declare_parameter('v_max', 0.5).value          # m/s
        self.W_MAX = self.declare_parameter('w_max', 1.2).value          # rad/s
        self.DEADMAN_TIMEOUT = self.declare_parameter('deadman_timeout_s', 0.35).value
        self.CMD_RATE = self.declare_parameter('cmd_rate_hz', 10.0).value

        # === 2) 상태 ===
        self.is_map_received = False
        self.goal_points = []
        self.current_goal_index = -1
        self.last_cmd_time = self.get_clock().now()

        # === 3) Rosmaster 연결 ===
        self.bot = None
        try:
            self.bot = Rosmaster(car_type=self.car_type, com=self.serial_port)
            self.get_logger().info(f"Rosmaster 연결 성공: {self.serial_port}")
        except Exception as e:
            self.get_logger().error(f"Rosmaster 연결 실패: {e}")
            self._emergency_stop()
            return

        # === 4) TF ===
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # === 5) 구독/타이머 ===
        self.map_subscriber = self.create_subscription(
            OccupancyGrid, '/map', self.map_callback, 10
        )
        self.timer = self.create_timer(0.1, self.control_loop)

        # 데드맨(워치독): 최근 명령이 DEADMAN_TIMEOUT 넘으면 자동 정지
        wd_period = 1.0 / max(self.CMD_RATE, 1.0)
        self.watchdog_timer = self.create_timer(wd_period, self._deadman_watchdog)

        # === 6) 안전 훅 (rclpy.on_shutdown 없이) ===
        atexit.register(self._emergency_stop)                 # 프로세스 종료 시
        signal.signal(signal.SIGINT, self._sigint_handler)    # Ctrl+C
        try:
            signal.signal(signal.SIGTERM, self._sigterm_handler)  # kill 등
        except Exception:
            pass

        self.get_logger().info("초기화 완료. /map 토픽을 기다립니다...")

    # ------------------------
    # 콜백/루프
    # ------------------------
    def map_callback(self, msg: OccupancyGrid):
        if self.is_map_received:
            return

        self.get_logger().info("맵 정보 수신 완료! 목표 지점을 계산합니다.")
        self.is_map_received = True

        width_m  = msg.info.width * msg.info.resolution
        height_m = msg.info.height * msg.info.resolution
        origin_x = msg.info.origin.position.x
        origin_y = msg.info.origin.position.y

        margin = self.MAP_MARGIN
        self.goal_points = [
            {'x': origin_x + margin,           'y': origin_y + margin},
            {'x': origin_x + width_m - margin, 'y': origin_y + margin},
            {'x': origin_x + width_m - margin, 'y': origin_y + height_m - margin},
            {'x': origin_x + margin,           'y': origin_y + height_m - margin}
        ]
        self.get_logger().info(f"계산된 목표 지점: {self.goal_points}")
        self.current_goal_index = 0
        self.get_logger().info("순찰을 시작합니다!")

    def control_loop(self):
        if not self.is_map_received or self.current_goal_index == -1:
            return

        try:
            # TF 조회: map -> base_link
            t = self.tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
            robot_x = t.transform.translation.x
            robot_y = t.transform.translation.y
            q = t.transform.rotation
            _, _, robot_yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])
        except TransformException as ex:
            self.get_logger().warn(f'TF 변환 실패: {ex}')
            self.send_motor_command(0.0, 0.0, 0.0)
            return
        except Exception as ex:
            self.get_logger().error(f'제어 루프 예외: {ex}')
            self.send_motor_command(0.0, 0.0, 0.0)
            return

        target_goal = self.goal_points[self.current_goal_index]
        dx = target_goal['x'] - robot_x
        dy = target_goal['y'] - robot_y
        dist_error = math.hypot(dx, dy)
        angle_to_goal = math.atan2(dy, dx)
        angle_error = math.atan2(math.sin(angle_to_goal - robot_yaw),
                                 math.cos(angle_to_goal - robot_yaw))

        # 도착 판정
        if dist_error < self.GOAL_TOLERANCE_DIST:
            self.get_logger().info(f"목표 지점 {self.current_goal_index + 1} 도착!")
            self.send_motor_command(0.0, 0.0, 0.0)
            self.current_goal_index = (self.current_goal_index + 1) % len(self.goal_points)
            self.get_logger().info(f"다음 목표({self.current_goal_index + 1})로 이동합니다...")
            time.sleep(2.0)  # 다음 목표 전 대기
            return

        # 간단 P 제어
        vx, wz = 0.0, 0.0
        if abs(angle_error) > self.GOAL_TOLERANCE_ANGLE:
            wz = self.P_GAIN_ANGULAR * angle_error
        else:
            vx = self.P_GAIN_LINEAR * dist_error
            wz = self.P_GAIN_ANGULAR * angle_error

        self.send_motor_command(vx, 0.0, wz)

    # ------------------------
    # 안전/유틸
    # ------------------------
    def send_motor_command(self, vx, vy, wz):
        """속도 포화 + 데드맨 타임스탬프 갱신."""
        if self.bot is None:
            return
        # 속도 포화
        vx = max(min(vx,  self.V_MAX), -self.V_MAX)
        wz = max(min(wz,  self.W_MAX), -self.W_MAX)
        try:
            self.bot.set_car_motion(vx, vy, wz)
        finally:
            self.last_cmd_time = self.get_clock().now()

    def _deadman_watchdog(self):
        """최근 모션 명령이 DEADMAN_TIMEOUT 이상 갱신되지 않으면 자동 정지."""
        now = self.get_clock().now()
        dt = (now - self.last_cmd_time).nanoseconds / 1e9
        if dt > self.DEADMAN_TIMEOUT:
            try:
                if self.bot is not None:
                    self.bot.set_car_motion(0.0, 0.0, 0.0)
            except Exception:
                pass

    def _emergency_stop(self, *args, **kwargs):
        """모든 종료 경로에서 호출되는 최후 방어 정지."""
        try:
            if self.bot is not None:
                self.bot.set_car_motion(0.0, 0.0, 0.0)
        except Exception:
            pass  # 종료 중 예외는 무시

    def _sigint_handler(self, signum, frame):
        self._emergency_stop()
        raise KeyboardInterrupt

    def _sigterm_handler(self, signum, frame):
        self._emergency_stop()
        raise SystemExit

    # ------------------------
    # 종료 오버라이드
    # ------------------------
    def destroy_node(self):
        self.get_logger().info("노드 종료. 로봇을 정지합니다.")
        self._emergency_stop()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = MapBasedPatrolNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # ✅ rclpy.ok() 여부와 무관하게 항상 정지/종료
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
