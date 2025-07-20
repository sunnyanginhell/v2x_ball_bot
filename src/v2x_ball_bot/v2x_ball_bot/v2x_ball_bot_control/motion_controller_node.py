import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist  # 로봇 속도 명령 메시지

class MotionControllerNode(Node):
    def __init__(self):
        super().__init__('motion_controller_node')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',  # 속도 명령을 받을 토픽 이름
            self.cmd_vel_callback,
            10
        )

    def cmd_vel_callback(self, msg):
        # 실제 모터 제어 코드로 대체
        self.get_logger().info(
            f'받은 속도 명령: linear={msg.linear.x}, angular={msg.angular.z}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = MotionControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()