#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
import math


class ObstacleDetectionNode(Node):
    def __init__(self):
        super().__init__('obstacle_detection_node')

        # 파라미터
        self.declare_parameter('range_threshold', 0.35)     # 장애물 감지 거리 (m)
        self.declare_parameter('angle_window_deg', 15.0)    # 전방 각도 범위 (deg)
        self.declare_parameter('angle_offset_deg', 180.0)   # 라이다 정면 보정 각도 (deg)

        self.range_threshold = self.get_parameter('range_threshold').value
        self.angle_window = math.radians(
            self.get_parameter('angle_window_deg').value
        )
        self.angle_offset = math.radians(
            self.get_parameter('angle_offset_deg').value
        )

        # 구독자 & 퍼블리셔
        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10
        )
        self.pub = self.create_publisher(Bool, '/dynamic_obstacle_detect', 10)

        self.get_logger().info(
            f"✅ ObstacleDetectionNode started "
            f"(threshold={self.range_threshold} m, "
            f"window=±{math.degrees(self.angle_window):.1f}°, "
            f"offset={math.degrees(self.angle_offset):.1f}°)"
        )

    def scan_callback(self, msg: LaserScan):
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment
        ranges = msg.ranges

        # 로봇 정면 기준 각도 범위 (offset 적용)
        min_angle = self.angle_offset - self.angle_window
        max_angle = self.angle_offset + self.angle_window

        obstacle_detected = False
        for i, r in enumerate(ranges):
            angle = angle_min + i * angle_increment

            if min_angle <= angle <= max_angle:
                if math.isinf(r) or r <= msg.range_min:
                    continue

                if r < self.range_threshold:
                    self.get_logger().info(
                        f"⚠️ Obstacle at {r:.3f} m, angle {math.degrees(angle):.1f}°"
                    )
                    obstacle_detected = True
                    break

        msg_out = Bool()
        msg_out.data = obstacle_detected
        self.pub.publish(msg_out)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleDetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
