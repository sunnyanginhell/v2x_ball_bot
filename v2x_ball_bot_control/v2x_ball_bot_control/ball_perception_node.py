#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from v2x_ball_bot_msgs.msg import Ball, BallArray
from visualization_msgs.msg import MarkerArray
from cv_bridge import CvBridge
import message_filters
import os

from v2x_ball_bot_control.ball_perception import (
    BallDetector, DepthMapper, SimpleTracker,
    make_marker, make_delete_all_marker
)


class BallPerceptionNode(Node):
    def __init__(self):
        super().__init__('ball_perception_node')

        package_dir = os.path.dirname(__file__)
        self.detector = BallDetector(package_dir)
        self.bridge = CvBridge()

        # 파라미터 설정
        self.rgb_topic = self.declare_parameter('rgb_topic', '/color/image_raw').value
        self.depth_topic = self.declare_parameter('depth_topic', '/depth/image_raw').value
        self.camera_info_topic = self.declare_parameter('camera_info_topic', '/color/camera_info').value
        self.publish_frame = self.declare_parameter('publish_frame', 'map').value

        # 카메라 intrinsic
        self.fx = self.fy = self.cx = self.cy = None
        self.create_subscription(CameraInfo, self.camera_info_topic, self.camera_info_callback, 10)

        # TF 버퍼
        import tf2_ros
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # RGB + Depth 동기화
        self.rgb_sub = message_filters.Subscriber(self, Image, self.rgb_topic)
        self.depth_sub = message_filters.Subscriber(self, Image, self.depth_topic)
        self.sync = message_filters.ApproximateTimeSynchronizer([self.rgb_sub, self.depth_sub], 10, 0.05)
        self.sync.registerCallback(self.synced_callback)

        # 퍼블리셔
        self.balls_pub = self.create_publisher(BallArray, '/balls', 10)
        self.markers_pub = self.create_publisher(MarkerArray, '/ball_markers', 10)

        # 트래커
        self.tracker = SimpleTracker()

    def camera_info_callback(self, msg):
        self.fx, self.fy, self.cx, self.cy = msg.k[0], msg.k[4], msg.k[2], msg.k[5]
        self.get_logger().info(
            f"[DEBUG] Camera Info loaded: fx={self.fx}, fy={self.fy}, cx={self.cx}, cy={self.cy}"
        )

    def synced_callback(self, rgb_msg, depth_msg):
        if self.fx is None:
            self.get_logger().warn("[DEBUG] Camera intrinsics not received yet")
            return

        try:
            color_img = self.bridge.imgmsg_to_cv2(rgb_msg, desired_encoding='bgr8')
            depth_img = self.bridge.imgmsg_to_cv2(depth_msg, desired_encoding='passthrough')
        except Exception as e:
            self.get_logger().error(f"이미지 변환 실패: {e}")
            return

        boxes, scores, vis_img = self.detector.detect(color_img)
        if len(boxes) == 0:
            self.get_logger().info("[DEBUG] No detections from YOLO")
            return

        mapper = DepthMapper(self.fx, self.fy, self.cx, self.cy, self.tf_buffer, self.publish_frame)
        ball_array = BallArray()
        ball_array.stamp = rgb_msg.header.stamp
        markers = MarkerArray()
        markers.markers.append(make_delete_all_marker(self.publish_frame, self.get_clock().now().to_msg()))

        # 가장 첫 번째 공만 처리
        box, score = boxes[0], scores[0]
        if score >= 0.3:
            p_map = mapper.pixel_to_map(box, depth_img, rgb_msg, self.get_logger())
            if p_map:
                ball_msg = Ball()
                ball_msg.stamp = rgb_msg.header.stamp
                ball_msg.id = "0"

                # 실제 좌표 그대로 사용
                ball_msg.x = p_map.point.x
                ball_msg.y = p_map.point.y
                ball_msg.z = p_map.point.z  # depth로 출력

                ball_msg.score = float(score)
                _, ball_msg.is_static = self.tracker.update(
                    0, ball_msg.x, ball_msg.y, rgb_msg.header.stamp.sec
                )

                # ✅ 좌표와 점수 로그 출력 (z → depth)
                self.get_logger().info(
                    f"[YOLO DETECTION] x={ball_msg.x:.3f}, y={ball_msg.y:.3f}, depth={ball_msg.z:.3f}, score={ball_msg.score:.2f}"
                )

                ball_array.balls.append(ball_msg)
                markers.markers.append(
                    make_marker(ball_msg, self.publish_frame, self.get_clock().now().to_msg())
                )

        self.balls_pub.publish(ball_array)
        self.markers_pub.publish(markers)


def main(args=None):
    rclpy.init(args=args)
    node = BallPerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
