import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # 예시: 장애물 회피 명령을 String으로 publish

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_node')
        self.publisher_ = self.create_publisher(String, 'obstacle_avoidance', 10)
        self.timer = self.create_timer(1.0, self.avoid_obstacle)

    def avoid_obstacle(self):
        msg = String()
        msg.data = 'Avoiding obstacle!'  # 실제 회피 로직으로 대체
        self.publisher_.publish(msg)
        self.get_logger().info('Published obstacle avoidance command')

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()