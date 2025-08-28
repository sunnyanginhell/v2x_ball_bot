#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from v2x_ball_bot_msgs.msg import Ball, BallArray
from cv_bridge import CvBridge
import message_filters, os

from v2x_ball_bot_control.ball_perception import BallDetector, DepthMapper, SimpleTracker
from std_msgs.msg import Header

class BallPerceptionNode(Node):
    def __init__(self):
        super().__init__('ball_perception_node')

        package_dir = os.path.dirname(__file__)
        self.detector = BallDetector(package_dir)
        self.bridge = CvBridge()

        # 파라미터
        self.rgb_topic = self.declare_parameter('rgb_topic', '/color/image_raw').value
        self.depth_topic = self.declare_parameter('depth_topic', '/depth/image_raw').value
        self.camera_info_topic = self.declare_parameter('camera_info_topic', '/color/camera_info').value
        self.publish_frame = self.declare_parameter('publish_frame', 'base_link').value

        self.fx = self.fy = self.cx = self.cy = None
        self.create_subscription(CameraInfo, self.camera_info_topic, self.camera_info_callback, 10)

        # TF
        import tf2_ros
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # 동기화
        self.rgb_sub = message_filters.Subscriber(self, Image, self.rgb_topic)
        self.depth_sub = message_filters.Subscriber(self, Image, self.depth_topic)
        self.sync = message_filters.ApproximateTimeSynchronizer([self.rgb_sub, self.depth_sub], 10, 0.05)
        self.sync.registerCallback(self.synced_callback)

        # Publisher
        self.balls_pub = self.create_publisher(BallArray, '/selected_ball', 10)
        self.debug_img_pub = self.create_publisher(Image, '/debug/ball_detection', 10)

        self.tracker = SimpleTracker()

    def camera_info_callback(self, msg):
        self.fx, self.fy, self.cx, self.cy = msg.k[0], msg.k[4], msg.k[2], msg.k[5]
        self.get_logger().info(f"[DEBUG] Camera Info loaded: fx={self.fx}, fy={self.fy}, cx={self.cx}, cy={self.cy}")

    def synced_callback(self, rgb_msg, depth_msg):
        if self.fx is None:
            return
        try:
            color_img = self.bridge.imgmsg_to_cv2(rgb_msg, 'bgr8')
            depth_img = self.bridge.imgmsg_to_cv2(depth_msg, 'passthrough')
        except Exception as e:
            self.get_logger().error(f"이미지 변환 실패: {e}")
            return

        boxes, scores, vis_img = self.detector.detect(color_img)

        ball_array = BallArray()
        ball_array.stamp = rgb_msg.header.stamp

        for i, (box, score) in enumerate(zip(boxes, scores)):
            if score < 0.6:  # ✅ 0.6 이하 제거
                continue

            mapper = DepthMapper(self.fx, self.fy, self.cx, self.cy, self.tf_buffer, self.publish_frame)
            p_map = mapper.pixel_to_map(box, depth_img, rgb_msg, self.get_logger())
            if not p_map:
                continue

            ball_msg = Ball()
            ball_msg.stamp = rgb_msg.header.stamp
            ball_msg.id = str(i)
            ball_msg.x, ball_msg.y, ball_msg.z = p_map.point.x, p_map.point.y, p_map.point.z
            ball_msg.score = float(score)
            _, ball_msg.is_static = self.tracker.update(i, ball_msg.x, ball_msg.y, rgb_msg.header.stamp.sec)
            ball_array.balls.append(ball_msg)

        self.balls_pub.publish(ball_array)

        # ✅ 디버깅 이미지 퍼블리시
        debug_msg = self.bridge.cv2_to_imgmsg(vis_img, encoding='bgr8')
        debug_msg.header = Header()
        debug_msg.header.stamp = self.get_clock().now().to_msg()
        self.debug_img_pub.publish(debug_msg)

def main(args=None):
    rclpy.init(args=args)
    node = BallPerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
