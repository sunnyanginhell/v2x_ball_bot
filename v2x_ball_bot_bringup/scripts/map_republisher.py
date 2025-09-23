#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from nav_msgs.msg import OccupancyGrid
import threading
import time
import copy

class MapRepublisher(Node):
    def __init__(self):
        super().__init__('map_republisher')

        # SUB: transient_local로 해서 map_server의 한 번 발행된 맵도 받음
        sub_qos = QoSProfile(depth=1)
        sub_qos.reliability = ReliabilityPolicy.RELIABLE
        sub_qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        self.sub = self.create_subscription(
            OccupancyGrid, '/map', self.map_cb, qos_profile=sub_qos)

        # PUB: TRANSIENT_LOCAL로 맞춤 -> 다른 구독자들이 TRANSIENT_LOCAL 기대하면 받음
        pub_qos = QoSProfile(depth=1)
        pub_qos.reliability = ReliabilityPolicy.RELIABLE
        pub_qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        self.pub = self.create_publisher(OccupancyGrid, '/map', qos_profile=pub_qos)

        self.last_map = None
        self.lock = threading.Lock()
        self.period_sec = 1.0
        self._logged_received = False

        self.get_logger().info('map_republisher started (republish every %.2f s)' % self.period_sec)

        t = threading.Thread(target=self._publisher_loop, daemon=True)
        t.start()

    def map_cb(self, msg: OccupancyGrid):
        with self.lock:
            # 안전하게 카피해서 저장
            self.last_map = copy.deepcopy(msg)
        if not self._logged_received:
            self.get_logger().info('Received initial /map (stored)')
            self._logged_received = True

    def _publisher_loop(self):
        # wait until rclpy initialized fully
        while rclpy.ok():
            with self.lock:
                m = self.last_map
            if m is not None:
                try:
                    # publish a copy to be safe
                    self.pub.publish(copy.deepcopy(m))
                except Exception as e:
                    self.get_logger().warn(f'Publish failed: {e}')
            time.sleep(self.period_sec)

def main(args=None):
    rclpy.init(args=args)
    node = MapRepublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
