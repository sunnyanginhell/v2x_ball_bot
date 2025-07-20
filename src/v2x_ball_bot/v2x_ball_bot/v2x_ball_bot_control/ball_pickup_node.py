import rclpy
from rclpy.node import Node

class BallPickupNode(Node):
    def __init__(self):
        super().__init__('ball_pickup_node')
        # 퍼블리셔/서브스크라이버/타이머 등 초기화
        self.get_logger().info('Ball Pickup Node started')

    def pickup_ball(self):
        # 공 집기 로직 구현
        pass

def main(args=None):
    rclpy.init(args=args)
    node = BallPickupNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()