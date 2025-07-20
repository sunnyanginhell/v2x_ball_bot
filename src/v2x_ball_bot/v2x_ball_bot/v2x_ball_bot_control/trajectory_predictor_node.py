# ball_detector_node로부터 받은 공의 위치 데이터를 기반으로, 공이 앞으로 어떻게 움직일지, 최종적으로 어디에 떨어질지를 예측하는 코드

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped, PoseStamped
from nav_msgs.msg import Path
from collections import deque
import numpy as np

class TrajectoryPredictorNode(Node):
    def __init__(self):
        """
        노드 초기화 함수
        """
        super().__init__('trajectory_predictor_node')

        # 파라미터 선언 및 초기화
        self.declare_parameter('min_points_for_prediction', 3)
        self.declare_parameter('prediction_horizon_sec', 1.5) # 몇 초 앞을 예측할지
        self.declare_parameter('prediction_frequency_hz', 20.0) # 예측 결과 발행 주기
        self.declare_parameter('gravity', 9.81) # 중력 가속도

        self.min_points = self.get_parameter('min_points_for_prediction').get_parameter_value().integer_value
        self.prediction_horizon = self.get_parameter('prediction_horizon_sec').get_parameter_value().double_value
        self.gravity = self.get_parameter('gravity').get_parameter_value().double_value
        
        # 최근 공 위치를 저장하기 위한 deque (최대 10개)
        self.ball_positions = deque(maxlen=10)

        # Subscriber: ball_detector_node로부터 공의 위치를 받음
        self.ball_position_subscriber = self.create_subscription(
            PointStamped,
            '/detected_ball',
            self.ball_position_callback,
            10)

        # Publisher: 예측된 궤적(Path)을 발행
        self.trajectory_publisher = self.create_publisher(Path, '/predicted_trajectory', 10)
        
        self.get_logger().info('Trajectory Predictor Node has been started.')

    def ball_position_callback(self, msg: PointStamped):
        """
        /detected_ball 토픽으로부터 메시지를 받았을 때 호출되는 콜백 함수
        """
        # 현재 시간과 함께 위치 데이터를 저장
        self.ball_positions.append(msg)
        
        # 예측을 위한 최소 데이터 포인트가 쌓였는지 확인
        if len(self.ball_positions) >= self.min_points:
            self.predict_and_publish_trajectory()

    def predict_and_publish_trajectory(self):
        """
        저장된 위치 데이터를 기반으로 궤적을 예측하고 발행하는 함수
        """
        # 가장 최근 두 개의 포인트로 속도를 추정
        if len(self.ball_positions) < 2:
            return

        p2 = self.ball_positions[-1] # 가장 최근 위치
        p1 = self.ball_positions[-2] # 바로 이전 위치

        # 시간 차이 계산 (nanoseconds to seconds)
        dt = (rclpy.time.Time.from_msg(p2.header.stamp) - rclpy.time.Time.from_msg(p1.header.stamp)).nanoseconds / 1e9
        
        # dt가 너무 작거나 0이면 계산 오류를 방지하기 위해 리턴
        if dt <= 1e-6:
            return

        # 속도 계산: (x2-x1)/dt
        vx = (p2.point.x - p1.point.x) / dt
        vy = (p2.point.y - p1.point.y) / dt
        vz = (p2.point.z - p1.point.z) / dt

        # Path 메시지 생성
        predicted_path = Path()
        predicted_path.header.stamp = self.get_clock().now().to_msg()
        predicted_path.header.frame_id = p2.header.frame_id # 기준 좌표계 설정

        # 예측 스텝 수 계산
        num_prediction_steps = int(self.prediction_horizon * self.get_parameter('prediction_frequency_hz').get_parameter_value().double_value)

        # 포물선 운동 공식으로 미래 위치 예측
        for i in range(num_prediction_steps):
            t = (i + 1) / self.get_parameter('prediction_frequency_hz').get_parameter_value().double_value
            
            # x(t) = x0 + v0_x * t
            pred_x = p2.point.x + vx * t
            # y(t) = y0 + v0_y * t
            pred_y = p2.point.y + vy * t
            # z(t) = z0 + v0_z * t - 0.5 * g * t^2
            pred_z = p2.point.z + vz * t - 0.5 * self.gravity * (t**2)

            # 공이 바닥(z=0) 아래로 떨어지면 예측 중단
            if pred_z < 0:
                break
                
            pose = PoseStamped()
            pose.header.stamp = rclpy.time.Time(seconds=self.get_clock().now().seconds_nanoseconds()[0], nanoseconds=self.get_clock().now().seconds_nanoseconds()[1] + t * 1e9).to_msg()
            pose.header.frame_id = predicted_path.header.frame_id
            pose.pose.position.x = pred_x
            pose.pose.position.y = pred_y
            pose.pose.position.z = pred_z
            # 방향(orientation)은 간단히 0으로 설정
            pose.pose.orientation.w = 1.0 
            
            predicted_path.poses.append(pose)

        # 예측된 경로 발행
        self.trajectory_publisher.publish(predicted_path)
        self.get_logger().info(f'Published predicted trajectory with {len(predicted_path.poses)} points.')


def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryPredictorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
