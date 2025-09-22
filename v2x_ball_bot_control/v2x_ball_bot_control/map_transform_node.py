#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped, PoseStamped
from tf2_ros import Buffer, TransformListener
from tf2_geometry_msgs import do_transform_point

class BallGoalTransform(Node):
    """
    입력: base_link 기준 공 좌표(PointStamped), 예: /ball_point_base
    출력: map 기준 목표(PoseStamped), 토픽: /ball_goal_in_map
    """
    def __init__(self):
        super().__init__('ball_goal_transform')
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)

        # 필요시 파라미터로 토픽명/프레임 바꾸세요.
        self.declare_parameter('input_topic', '/ball_point_base')
        self.declare_parameter('target_frame', 'map')

        input_topic = self.get_parameter('input_topic').get_parameter_value().string_value
        self.target_frame = self.get_parameter('target_frame').get_parameter_value().string_value

        self.sub = self.create_subscription(PointStamped, input_topic, self.cb, 10)
        self.pub_goal = self.create_publisher(PoseStamped, '/ball_goal_in_map', 10)

    def cb(self, msg_base: PointStamped):
        try:
            # msg_base.header.frame_id는 반드시 "base_link" 여야 합니다.
            tf = self.buffer.lookup_transform(
                self.target_frame,                # target: map
                msg_base.header.frame_id,         # source: base_link (또는 camera_link 등)
                rclpy.time.Time())                # 최신 변환 사용

            pt_in_map = do_transform_point(msg_base, tf)

            goal = PoseStamped()
            goal.header.stamp = self.get_clock().now().to_msg()
            goal.header.frame_id = self.target_frame
            goal.pose.position.x = pt_in_map.point.x
            goal.pose.position.y = pt_in_map.point.y
            goal.pose.position.z = 0.0
            goal.pose.orientation.w = 1.0  # 필요시 yaw로 세팅
            self.pub_goal.publish(goal)

        except Exception as e:
            self.get_logger().warn(f'[ball_goal_transform] TF failed: {e}')

def main():
    rclpy.init()
    node = BallGoalTransform()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
