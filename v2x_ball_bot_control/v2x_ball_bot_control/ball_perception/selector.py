#!/usr/bin/env python3
import rclpy, math
from rclpy.node import Node
from v2x_ball_bot_msgs.msg import BallArray, Ball

class BallSelector(Node):
    def __init__(self):
        super().__init__('ball_selector')
        self.sub = self.create_subscription(BallArray, '/balls', self.callback, 10)
        self.pub = self.create_publisher(BallArray, '/selected_ball', 10)

        self.selected_ball = None   # ✅ 최초 선택된 공 저장
        self.published = False      # ✅ 이미 퍼블리시했는지 플래그

    def callback(self, msg: BallArray):
        if self.published:  # ✅ 이미 선택했으면 더는 실행 안 함
            return
        if not msg.balls:
            return

        # ✅ 후보 필터링 (정확도 0.6 이상만)
        filtered = [b for b in msg.balls if b.score >= 0.6]
        if not filtered:
            self.get_logger().info("[SELECTOR] No ball passed the threshold (score>=0.6)")
            return

        # ✅ 점수 = 거리 역수 + 정확도
        candidates = []
        for b in filtered:
            dist = math.sqrt(b.x**2 + b.y**2 + b.z**2)
            weight = (1.0 / (dist + 1e-6)) + b.score
            candidates.append((weight, b))

        best = max(candidates, key=lambda x: x[0])[1]
        self.selected_ball = best

        # ✅ BallArray로 감싸서 퍼블리시 (한 번만)
        selected_msg = BallArray()
        selected_msg.stamp = msg.stamp
        selected_msg.balls.append(best)

        self.pub.publish(selected_msg)
        self.get_logger().info(
            f"[SELECTOR] Selected Ball ID={best.id}, dist={math.sqrt(best.x**2+best.y**2+best.z**2):.2f}, "
            f"score={best.score:.2f} → FIXED"
        )

        self.published = True  # ✅ 이후에는 새로 퍼블리시 안 함

def main(args=None):
    rclpy.init(args=args)
    node = BallSelector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
