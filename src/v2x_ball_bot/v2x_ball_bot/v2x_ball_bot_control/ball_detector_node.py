import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # 예시: 감지 결과를 String으로 publish

class BallDetectorNode(Node):
    def __init__(self):
        super().__init__('ball_detector_node')
        self.publisher_ = self.create_publisher(String, 'ball_detection', 10)
        self.timer = self.create_timer(1.0, self.detect_ball)

    def detect_ball(self):
        msg = String()
        msg.data = 'Ball detected!'  # 실제 감지 로직으로 대체
        self.publisher_.publish(msg)
        self.get_logger().info('Published ball detection result')

def main(args=None):
    rclpy.init(args=args)
    node = BallDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()