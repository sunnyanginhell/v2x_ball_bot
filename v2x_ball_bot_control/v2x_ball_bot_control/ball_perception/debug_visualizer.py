#!/usr/bin/env python3
import rclpy, cv2
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class DebugVisualizer(Node):
    def __init__(self):
        super().__init__('debug_visualizer')
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, '/debug/ball_detection', self.callback, 10)

    def callback(self, msg: Image):
        try:
            img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            cv2.imshow("Ball Detection Debug", img)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f"디버깅 이미지 표시 실패: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = DebugVisualizer()
    rclpy.spin(node)
    node.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
