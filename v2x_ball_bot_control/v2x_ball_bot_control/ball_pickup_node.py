#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import serial
import time

from v2x_ball_bot_control.rosmaster import Rosmaster

class BallPickupNode(Node):
    def __init__(self):
        super().__init__('ball_pickup_node')
        self.get_logger().info('공 수거 노드 초기화 시작')

        # 파라미터 선언
        self.opencr_port = self.declare_parameter('opencr_port', '/dev/ttyACM0').value
        #serial_port 뭐 에러뜨면 ttyUSB1으로 실행해보기.
        self.serial_port = self.declare_parameter('serial_port', '/dev/ttyUSB0').value
        self.car_type = self.declare_parameter('car_type', 1).value

        # 상태 변수
        self.is_picking_up = False

        # Rosmaster 초기화
        self.bot = None
        try:
            self.bot = Rosmaster(car_type=self.car_type, com=self.serial_port)
            self.bot.create_receive_threading()
            time.sleep(0.1)
            self.bot.set_car_type(self.car_type)
            self.get_logger().info(f"Rosmaster 시리얼 포트 연결 성공: {self.serial_port}")
        except Exception as e:
            self.get_logger().error(f"Rosmaster 시리얼 포트 연결 실패: {e}")

        # OpenCR 시리얼 포트 초기화
        self.opencr_serial = None
        try:
            self.opencr_serial = serial.Serial(self.opencr_port, 115200, timeout=1.0)
            time.sleep(2)
            self.get_logger().info(f"OpenCR 시리얼 포트 연결 성공: {self.opencr_port}")
        except Exception as e:
            self.get_logger().error(f"OpenCR 시리얼 포트 연결 실패: {e}")

        # ROS I/O
        self.sub_pickup = self.create_subscription(
            Bool, '/pickup_command', self.pickup_callback, 10)
        # ✅ Follower 노드에 작업 완료를 알릴 퍼블리셔 추가
        self.pub_complete = self.create_publisher(Bool, '/pickup_complete', 10)

        self.get_logger().info("초기화 완료. 수거 명령 대기 중...")

    def pickup_callback(self, msg: Bool):
        if msg.data and not self.is_picking_up:
            #이제부터 픽업을 수행하겠다고 True로 선언해주기
            self.is_picking_up = True
            self.get_logger().info("수거 명령 수신! 공 수거 시퀀스를 시작합니다.")
            #픽업 작업을 실제로 수행하는 함수를 실행시키기
            self.execute_pickup_sequence()

    def execute_pickup_sequence(self):
        if self.bot is None:
            self.get_logger().error("Rosmaster가 연결되지 않아 동작을 실행할 수 없습니다.")
            self.is_picking_up = False
            return

        # 1. 그리퍼 내리기
        self.get_logger().info("1. 그리퍼 내리기 명령 전송 ('1')")
        self.opencr_port.write(b'1')
        time.sleep(2.0)

        # 2. 뒤로 1미터 이동
        self.get_logger().info("2. 약 1미터 후진 시작")
        backward_speed = -0.2
        duration = 5.0

        self.bot.set_car_motion(backward_speed, 0.0, 0.0)
        time.sleep(duration)
        self.bot.set_car_motion(0.0, 0.0, 0.0)
        self.get_logger().info("후진 완료.")
        time.sleep(0.5)

        # 3. 그리퍼 올리기
        self.get_logger().info("3. 그리퍼 올리기 명령 전송 ('0')")
        self.opencr_port.write(b'0')
        time.sleep(2.0)

        # ✅ 4. 작업 완료 신호 전송
        self.get_logger().info("공 수거 시퀀스 완료. Follower에 완료 신호 전송.")
        complete_msg = Bool()
        complete_msg.data = True
        self.pub_complete.publish(complete_msg)

        self.is_picking_up = False

    def send_gripper_command(self, command: str):
        if self.opencr_serial and self.opencr_serial.is_open:
            self.opencr_serial.write(command.encode('utf-8'))
        else:
            self.get_logger().warn("OpenCR 시리얼 포트가 연결되지 않았습니다.")

    def destroy_node(self):
        self.get_logger().info("노드 종료.")
        if self.opencr_serial and self.opencr_serial.is_open:
            self.opencr_serial.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = BallPickupNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
