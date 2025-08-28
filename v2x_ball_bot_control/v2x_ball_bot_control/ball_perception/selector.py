#!/usr/bin/env python3
import rclpy, math
from rclpy.node import Node
from v2x_ball_bot_msgs.msg import BallArray, Ball

class BallSelector(Node):
    def __init__(self):
        super().__init__('ball_selector')
        self.sub = self.create_subscription(BallArray, '/balls', self.callback, 10)
        self.pub = self.create_publisher(BallArray, '/selected_ball', 10)

    def callback(self, msg: BallArray):
        if not msg.balls:
            return

        # ✅ 점수 = 거리 역수 + 정확도
        candidates = []
        for b in msg.balls:
            dist = math.sqrt(b.x**2 + b.y**2 + b.z**2)
            score = (1.0 / (dist + 1e-6)) + b.score
            candidates.append((score, b))

        best = max(candidates, key=lambda x: x[0])[1]

        selected = BallArray()
        selected.stamp = msg.stamp
        selected.balls.append(best)

        self.get_logger().info(f"[SELECTOR] Selected Ball ID={best.id}, dist={math.sqrt(best.x**2+best.y**2+best.z**2):.2f}, score={best.score:.2f}")
        self.pub.publish(selected)

def main(args=None):
    rclpy.init(args=args)
    node = BallSelector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
