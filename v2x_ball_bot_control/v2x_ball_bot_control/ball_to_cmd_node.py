#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from typing import Optional

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
# Ball.msg (사용자 정의)
from v2x_ball_bot_msgs.msg import Ball

def clamp(x, lo, hi): return max(lo, min(hi, x))

class BallToCmd(Node):
    """
    base_link 기준 Ball (x,y,z) → /cmd_vel_out
    - v = k_v * (d - target_dist),  w = k_w * heading
    - heading = atan2(y, x), d = z(신뢰되면) or sqrt(x^2 + y^2)
    - 후진 금지(양의 v만), 한계 속도/각속도 적용
    - is_static 옵션/타임아웃/E-STOP 반영
    """
    def __init__(self):
        super().__init__('ball_to_cmd')

        # ----- Parameters -----
        self.ball_topic   = self.declare_parameter('ball_topic', '/ball').value
        self.cmd_topic    = self.declare_parameter('cmd_topic',  '/cmd_vel_out').value
        self.estop_topic  = self.declare_parameter('estop_topic','/safety/estop').value

        self.k_v          = float(self.declare_parameter('k_v', 0.8).value)
        self.k_w          = float(self.declare_parameter('k_w', 1.2).value)
        self.target_dist  = float(self.declare_parameter('target_dist_m', 0.60).value)
        self.v_max        = float(self.declare_parameter('v_max', 0.35).value)
        self.w_max        = float(self.declare_parameter('w_max', 0.60).value)
        self.deadband_yaw = float(self.declare_parameter('deadband_yaw_deg', 5.0).value)   # 정렬 완료 기준
        self.stop_margin  = float(self.declare_parameter('stop_margin_m',   0.05).value)   # 정지 거리 여유
        self.only_static  = bool(self.declare_parameter('use_static_only', False).value)   # 정지공만 추종
        self.ball_timeout = float(self.declare_parameter('ball_timeout_sec', 1.0).value)   # 수신 끊기면 정지
        self.yaw_slowdeg  = float(self.declare_parameter('yaw_slow_deg', 10.0).value)      # 헤딩 크면 v 감쇠
        self.slow_gain    = float(self.declare_parameter('slow_gain', 0.5).value)          # 감쇠 비율

        # ----- IO -----
        self.pub_cmd = self.create_publisher(Twist, self.cmd_topic, 10)
        self.sub_estop = self.create_subscription(Bool, self.estop_topic, self.on_estop, 10)
        self.sub_ball  = self.create_subscription(Ball, self.ball_topic, self.on_ball, 10)

        # ----- State -----
        self.estop = False
        self.last_ball_xy: Optional[tuple[float, float]] = None
        self.last_ball_z: Optional[float] = None
        self.last_stamp_sec: float = 0.0

        # 20Hz 주기 발행(안전)
        self.timer = self.create_timer(0.05, self.on_timer)

        self.get_logger().info(
            f"BallToCmd ready. sub:{self.ball_topic}, pub:{self.cmd_topic} (A-plan: motor_driver=serial)"
        )

    def on_estop(self, msg: Bool):
        self.estop = bool(msg.data)

    def on_ball(self, msg: Ball):
        # 정지공만 추종 설정 시, 움직이는 공이면 무시
        if self.only_static and not msg.is_static:
            return

        # base_link 기준 좌표
        x, y, z = float(msg.x), float(msg.y), float(msg.z)

        # 수신 저장
        self.last_ball_xy = (x, y)
        # z가 유효하면 저장(>0)
        self.last_ball_z = z if z > 0.0 else None
        self.last_stamp_sec = self.get_clock().now().nanoseconds * 1e-9

    def on_timer(self):
        # 안전 정지 조건
        if self.estop or self._timed_out():
            self.pub_cmd.publish(Twist()); return
        if self.last_ball_xy is None:
            self.pub_cmd.publish(Twist()); return

        x, y = self.last_ball_xy
        # 거리: Depth z를 신뢰할 수 있으면 우선 사용, 아니면 평면거리
        if self.last_ball_z is not None and self.last_ball_z > 0.0:
            dist = float(self.last_ball_z)
        else:
            dist = float(math.hypot(x, y))

        heading = math.atan2(y, x)  # 좌(+)/우(-) 편차 각(rad)

        # P제어
        v_cmd = self.k_v * (dist - self.target_dist)
        w_cmd = self.k_w * heading

        # heading이 크면 접근 속도 감쇠(먼저 회전 정렬)
        if abs(heading) > math.radians(self.yaw_slowdeg):
            v_cmd *= self.slow_gain

        # 제한(후진 금지)
        v_cmd = clamp(v_cmd, 0.0, self.v_max)
        w_cmd = clamp(w_cmd, -self.w_max, self.w_max)

        # 정지 조건(목표 근접 + 헤딩 정렬)
        if (dist <= self.target_dist + self.stop_margin) and (abs(heading) < math.radians(self.deadband_yaw)):
            v_cmd, w_cmd = 0.0, 0.0

        tw = Twist()
        tw.linear.x  = float(v_cmd)
        tw.angular.z = float(w_cmd)
        self.pub_cmd.publish(tw)

    def _timed_out(self) -> bool:
        if self.last_stamp_sec == 0.0:
            return True
        now = self.get_clock().now().nanoseconds * 1e-9
        return (now - self.last_stamp_sec) > self.ball_timeout

def main(args=None):
    rclpy.init(args=args)
    node = BallToCmd()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
