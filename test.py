#!/usr/bin/env python3
import time
# v2x_ball_bot_control 폴더에 rosmaster.py가 있다고 가정합니다.
# 만약 다른 위치에 있다면 경로를 맞게 수정해야 합니다.
from v2x_ball_bot_control.rosmaster import Rosmaster

# --- 설정 (사용자 환경에 맞게 수정) ---
# Rosmaster 보드가 연결된 시리얼 포트 이름
# `ls /dev/tty*` 명령어로 확인 가능 (보통 /dev/ttyUSB0 또는 /dev/ttyACM0)
SERIAL_PORT = "/dev/ttyUSB0"
# 차량 종류 (X3 모델의 경우 1)
CAR_TYPE = 1
# ------------------------------------

# bot 변수를 전역적으로 접근할 수 있도록 초기화
bot = None

try:
    # 1. Rosmaster 객체 생성 및 연결
    print(f"'{SERIAL_PORT}'에 연결을 시도합니다...")
    bot = Rosmaster(com=SERIAL_PORT, car_type=CAR_TYPE)
    bot.create_receive_threading() # 데이터 수신 스레드 시작
    time.sleep(0.1)
    bot.set_car_type(CAR_TYPE) # 차량 종류 설정
    print("Rosmaster 연결 성공!")

    # 2. 삑 소리로 연결 확인
    bot.set_beep(50) # 50ms 동안 삑 소리
    time.sleep(0.5)

    # 3. 앞으로 2초간 이동
    forward_speed = 0.2 # 초속 0.2미터 (천천히)
    move_duration = 2.0 # 2초 동안
    
    print(f"{forward_speed}m/s의 속도로 {move_duration}초간 전진합니다...")
    bot.set_car_motion(forward_speed, 0.0, 0.0)
    time.sleep(move_duration)

    # 4. 정지
    print("정지합니다.")
    bot.set_car_motion(0.0, 0.0, 0.0)
    time.sleep(1) # 확실히 정지할 시간을 줌

    print("테스트 완료.")

except Exception as e:
    print(f"오류가 발생했습니다: {e}")
    print("1. 시리얼 포트 이름이 올바른지 확인하세요.")
    print("2. Rosmaster 보드에 전원이 들어와 있는지 확인하세요.")
    print("3. 'sudo chmod 666 /dev/ttyUSB0' 와 같이 권한을 부여했는지 확인하세요.")

finally:
    # 5. 프로그램 종료 시 반드시 로봇을 정지
    if bot is not None:
        print("안전을 위해 로봇을 정지시키고 연결을 종료합니다.")
        bot.set_car_motion(0.0, 0.0, 0.0)
