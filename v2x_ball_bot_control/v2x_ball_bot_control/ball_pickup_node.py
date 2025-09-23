#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import serial
import time

# rosmaster.py는 사용자의 라이브러리로 가정합니다.
from v2x_ball_bot_control.rosmaster import Rosmaster

class BallPickupNode(Node):
    def __init__(self):
        super().__init__('ball_pickup_node')
        self.get_logger().info('공 수거 노드 초기화 시작')

        # 파라미터 선언
        self.opencr_port = self.declare_parameter('opencr_port', '/dev/ttyACM0').value
        self.serial_port = self.declare_parameter('serial_port', '/dev/ttyUSB1').value
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
            time.sleep(2) # OpenCR 부팅 및 시리얼 안정화 대기
            self.get_logger().info(f"OpenCR 시리얼 포트 연결 성공: {self.opencr_port}")
        except Exception as e:
            self.get_logger().error(f"OpenCR 시리얼 포트 연결 실패: {e}")

        # ROS I/O
        self.sub_pickup = self.create_subscription(
            Bool, '/pickup_command', self.pickup_callback, 10)
        self.pub_complete = self.create_publisher(Bool, '/pickup_complete', 10)

        self.get_logger().info("초기화 완료. 수거 명령 대기 중...")

    def pickup_callback(self, msg: Bool):
        if msg.data and not self.is_picking_up:
            self.is_picking_up = True
            self.get_logger().info("수거 명령 수신! 공 수거 시퀀스를 시작합니다.")
            self.execute_pickup_sequence()

    def execute_pickup_sequence(self):
        if self.bot is None or self.opencr_serial is None or not self.opencr_serial.is_open:
            self.get_logger().error("Rosmaster 또는 OpenCR이 연결되지 않아 동작을 실행할 수 없습니다.")
            self.is_picking_up = False
            return

        sequence_success = True

        # 1. 그리퍼 내리기
        self.get_logger().info("1. 그리퍼 내리기 시작")
        try:
            # 쓰기 전에 버퍼를 비워 통신 안정성을 높입니다.
            self.opencr_serial.reset_input_buffer()
            self.opencr_serial.write(b'1')
            self.get_logger().info(" -> '1' 명령 전송 완료")
            time.sleep(2.0)
        except serial.SerialException as e:
            self.get_logger().error(f"그리퍼 내리기 중 시리얼 오류 발생: {e}")
            sequence_success = False
        
        # 2. 후진 (앞선 단계가 성공했을 경우에만 실행)
        if sequence_success:
            self.get_logger().info("2. 약 1미터 후진 시작")
            try:
                backward_speed = -0.2
                duration = 5.0
                self.bot.set_car_motion(backward_speed, 0.0, 0.0)
                time.sleep(duration)
                self.bot.set_car_motion(0.0, 0.0, 0.0)
                self.get_logger().info(" -> 후진 완료.")
                time.sleep(0.5)
            except Exception as e:
                self.get_logger().error(f"후진 동작 중 오류 발생: {e}")
                sequence_success = False

        # 3. 그리퍼 올리기 (앞선 단계들이 모두 성공했을 경우에만 실행)
        if sequence_success:
            self.get_logger().info("3. 그리퍼 올리기 시작")
            try:
                self.opencr_serial.reset_input_buffer()
                self.opencr_serial.write(b'0')
                self.get_logger().info(" -> '0' 명령 전송 완료")
                time.sleep(2.0)
            except serial.SerialException as e:
                self.get_logger().error(f"그리퍼 올리기 중 시리얼 오류 발생: {e}")
                sequence_success = False

        # 4. 작업 완료 신호 전송 (모든 시퀀스가 성공했을 때만)
        if sequence_success:
            self.get_logger().info("공 수거 시퀀스 완료. Follower에 완료 신호 전송.")
            complete_msg = Bool()
            complete_msg.data = True
            self.pub_complete.publish(complete_msg)
        else:
            self.get_logger().error("공 수거 시퀀스 실패. 완료 신호를 보내지 않습니다.")

        # 성공하든 실패하든, 다음 명령을 받을 수 있도록 상태를 초기화합니다.
        self.is_picking_up = False

    def destroy_node(self):
        self.get_logger().info("노드 종료.")
        if self.opencr_serial and self.opencr_serial.is_open:
            self.opencr_serial.close()
        # if self.bot: self.bot.shutdown() # Rosmaster 종료 로직이 있다면 호출
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
