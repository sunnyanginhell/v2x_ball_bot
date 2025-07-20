import rclpy
from rclpy.node import Node

class PathPlannerNode(Node):
    def __init__(self):
        super().__init__('path_planner_node')
        # 퍼블리셔/서브스크라이버/타이머 등 초기화
        self.get_logger().info('Path Planner Node started')

    def plan_path(self, start, goal):
        # 경로 계획 알고리즘 구현 (예: A*, Dijkstra 등)
        pass

def main(args=None):
    rclpy.init(args=args)
    node = PathPlannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

# 추가할 기능
# 현재 위치와 목표 위치를 받는 서브스크라이버
# 경로 결과를 퍼블리시하는 퍼블리셔
# 경로 계획 알고리즘 구현