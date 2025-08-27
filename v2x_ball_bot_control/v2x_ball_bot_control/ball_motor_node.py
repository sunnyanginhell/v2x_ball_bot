#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ROS 2 Humble / rclpy
# base_link 기준 Ball(x,y,z) -> vx, vy, yaw(wz) 계산 후 Rosmaster.set_car_motion(vx, vy, wz)

import math
from typing import Optional

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from v2x_ball_bot_msgs.msg import Ball  # 사용자 정의 Ball.msg

def clamp(x, lo, hi): return max(lo, min(hi, x))

class BallMotorVXYW(Node):
    def __init__(self):
        super().__init__('ball_motor_vxyw')

        # ---------------- Params ----------------
        # Topics
        self.ball_topic   = self.declare_parameter('ball_topic', '/ball').value
        self.estop_topic  = self.declare_parameter('estop_topic', '/safety/estop').value
        self.debug_twist_topic = self.declare_parameter('debug_twist_topic', '/cmd_vel_debug').value

        # Control (Ball -> vx, vy, wz)
        self.k_v          = float(self.declare_parameter('k_v', 0.8).value)     # 거리 P게인
        self.k_w          = float(self.declare_parameter('k_w', 1.2).value)     # 헤딩 P게인
        self.target_dist  = float(self.declare_parameter('target_dist_m', 0.60).value)
        self.v_max        = float(self.declare_parameter('v_max', 0.35).value)  # m/s
        self.w_max        = float(self.declare_parameter('w_max', 0.60).value)  # rad/s
        self.yaw_slowdeg  = float(self.declare_parameter('yaw_slow_deg', 10.0).value)
        self.slow_gain    = float(self.declare_parameter('slow_gain', 0.5).value)

        self.deadband_yaw = float(self.declare_parameter('deadband_yaw_deg', 5.0).value)
        self.stop_margin  = float(self.declare_parameter('stop_margin_m', 0.05).value)
        self.only_static  = bool(self.declare_parameter('use_static_only', False).value)
        self.ball_timeout = float(self.declare_parameter('ball_timeout_sec', 1.0).value)
        self.depth_priority = bool(self.declare_parameter('use_depth_z_preferred', True).value)

        # Slew rate limits (가감속 제한)
        self.accel_v      = float(self.declare_parameter('accel_v', 0.8).value)  # m/s^2
        self.accel_w      = float(self.declare_parameter('accel_w', 1.5).value)  # rad/s^2

        # Serial (Rosmaster)
        self.serial_port  = self.declare_parameter('serial_port', '/dev/ttyUSB0').value
        self.serial_baud  = int(self.declare_parameter('serial_baud', 115200).value)
        self.car_type     = int(self.declare_parameter('car_type', 1).value)  # Rosmaster X3 = 1

        # ---------------- IO ----------------
        self.sub_ball  = self.create_subscription(Ball, self.ball_topic, self.on_ball, 10)
        self.sub_estop = self.create_subscription(Bool, self.estop_topic, self.on_estop, 10)
        self.pub_debug = self.create_publisher(Twist, self.debug_twist_topic, 10)

        # ---------------- State ----------------
        self.estop = False
        self.last_ball_xy: Optional[tuple[float, float]] = None
        self.last_ball_z: Optional[float] = None
        self.last_stamp_sec: float = 0.0

        # Slew internal states
        self.vx_cur = 0.0
        self.wz_cur = 0.0
        # vy는 차동구동 기본 0. 필요 시 오므니/메카넘용으로 제어식 추가.
        self.vy_cur = 0.0

        # Serial open
        self.bot = None
        try:
            from v2x_ball_bot_control.rosmaster import Rosmaster  # 패키지 경로로 임포트 권장
            self.bot = Rosmaster(car_type=self.car_type, com=self.serial_port)
            self.get_logger().info(f"Serial opened: {self.serial_port} @ {self.serial_baud} (car_type={self.car_type})")
        except Exception as e:
            self.get_logger().error(f"Serial open failed: {e}")
            self.bot = None

        # Timer (20 Hz)
        self.dt = 0.05
        self.timer = self.create_timer(self.dt, self.on_timer)

        self.get_logger().info("BallMotorVXYW ready. (direct set_car_motion)")

    # ---------------- Callbacks ----------------
    def on_estop(self, msg: Bool):
        self.estop = bool(msg.data)

    def on_ball(self, msg: Ball):
        if self.only_static and not msg.is_static:
            return
        self.last_ball_xy = (float(msg.x), float(msg.y))
        self.last_ball_z = float(msg.z) if msg.z > 0.0 else None
        self.last_stamp_sec = self.get_clock().now().nanoseconds * 1e-9

    # ---------------- Main loop ----------------
    def on_timer(self):
        # 기본 목표값
        vx_des, vy_des, wz_des = 0.0, 0.0, 0.0

        # 안전 정지
        if self.estop or self._timed_out() or self.last_ball_xy is None:
            self._apply_and_send(vx_des, vy_des, wz_des)
            return

        x, y = self.last_ball_xy
        # 거리 산정: Depth z를 신뢰하면 우선 사용, 아니면 평면거리
        if self.depth_priority and (self.last_ball_z is not None) and (self.last_ball_z > 0.0):
            dist = float(self.last_ball_z)
        else:
            dist = float(math.hypot(x, y))

        heading = math.atan2(y, x)  # +좌/ -우 (rad)

        # --- P 제어: 차동구동 기본 (vy=0.0) ---
        vx_des = self.k_v * (dist - self.target_dist)
        wz_des = self.k_w * heading

        # 헤딩 오차 크면 먼저 정렬: 전진 감쇠
        if abs(heading) > math.radians(self.yaw_slowdeg):
            vx_des *= self.slow_gain

        # 제한 (후진 금지)
        vx_des = clamp(vx_des, 0.0, self.v_max)
        wz_des = clamp(wz_des, -self.w_max, self.w_max)

        # 성공/정지 조건
        if (dist <= self.target_dist + self.stop_margin) and (abs(heading) < math.radians(self.deadband_yaw)):
            vx_des, vy_des, wz_des = 0.0, 0.0, 0.0

        # 가감속 제한(slew)
        vx_cmd = self._slew(self.vx_cur, vx_des, self.accel_v * self.dt)
        wz_cmd = self._slew(self.wz_cur, wz_des, self.accel_w * self.dt)
        vy_cmd = 0.0  # 차동구동: 0. (메카넘/옴니면 여기서 y 에러 기반 제어 추가)

        # 적용/전송
        self._apply_and_send(vx_cmd, vy_cmd, wz_cmd)

    # ---------------- Helpers ----------------
    def _timed_out(self) -> bool:
        if self.last_stamp_sec == 0.0:
            return True
        now = self.get_clock().now().nanoseconds * 1e-9
        return (now - self.last_stamp_sec) > self.ball_timeout

    def _slew(self, cur: float, des: float, step: float) -> float:
        if des > cur + step:
            return cur + step
        if des < cur - step:
            return cur - step
        return des

    def _apply_and_send(self, vx: float, vy: float, wz: float):
        # 상태 갱신
        self.vx_cur, self.vy_cur, self.wz_cur = float(vx), float(vy), float(wz)

        # 디버그 twist 발행(옵션)
        tw = Twist()
        tw.linear.x  = self.vx_cur
        tw.linear.y  = self.vy_cur
        tw.angular.z = self.wz_cur
        self.pub_debug.publish(tw)

        # 시리얼 전송
        if self.bot is None:
            return
        try:
            # Rosmaster API: set_car_motion(vx, vy, wz) 가정
            self.bot.set_car_motion(self.vx_cur, self.vy_cur, self.wz_cur)
        except Exception as e:
            self.get_logger().error(f"Serial write failed: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = BallMotorVXYW()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
