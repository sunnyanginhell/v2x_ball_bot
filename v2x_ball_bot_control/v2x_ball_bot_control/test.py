import time
import serial
# v2x_ball_bot_control 폴더에 rosmaster.py가 있다고 가정합니다.
# 만약 다른 위치에 있다면 경로를 맞게 수정해야 합니다.
from v2x_ball_bot_control.rosmaster import Rosmaster

# --- 설정 (사용자 환경에 맞게 수정) ---
# Rosmaster 보드가 연결된 시리얼 포트 이름
SERIAL_PORT = "/dev/ttyUSB1"
# OpenCR 보드가 연결된 시리얼 포트 이름
# OpenCR 코드에서 Serial1을 사용하므로, 라즈베리파이의 하드웨어 시리얼(/dev/ttyS0 또는 /dev/ttyAMA0)에
# 연결되었거나, USB 포트(/dev/ttyACM0)에 연결되었는지 확인하고 포트 이름을 맞춰야 합니다.
OPENCR_PORT = "/dev/ttyACM0"
# OpenCR 보드와 통신 속도 (OpenCR 코드의 115200과 일치)
BAUDRATE_OPENCR = 115200
# 차량 종류 (X3 모델의 경우 1)
CAR_TYPE = 1
# ------------------------------------

# bot과 ser_opencr 변수를 전역적으로 접근할 수 있도록 초기화
bot = None
ser_opencr = None

try:
    # 1. Rosmaster 객체 생성 및 연결
    print(f"'{SERIAL_PORT}' (Rosmaster)에 연결을 시도합니다...")
    bot = Rosmaster(com=SERIAL_PORT, car_type=CAR_TYPE)
    bot.create_receive_threading()
    time.sleep(1.0)
    bot.set_car_type(CAR_TYPE)
    print("Rosmaster 연결 성공!")
   
    # 2. OpenCR 보드와 시리얼 통신 연결
    print(f"'{OPENCR_PORT}' (OpenCR)에 {BAUDRATE_OPENCR} 속도로 연결을 시도합니다...")
    ser_opencr = serial.Serial(OPENCR_PORT, BAUDRATE_OPENCR, timeout=1)
    time.sleep(2) # OpenCR 보드가 리셋되고 안정화될 시간을 줌
    print("OpenCR 연결 성공!")

    # 3. 삑 소리로 연결 확인
    bot.set_beep(50)
    time.sleep(1.0)

    # 4. 앞으로 2초간 이동
    forward_speed = 0.2
    move_duration = 2.0
   
    print(f"{forward_speed}m/s의 속도로 {move_duration}초간 전진합니다...")
    bot.set_car_motion(forward_speed, 0.0, 0.0)
    time.sleep(move_duration)

    # 5. 정지
    print("정지합니다.")
    bot.set_car_motion(0.0, 0.0, 0.0)
    time.sleep(1)

    # 6. OpenCR 보드에 신호 보내기 (OpenCR 코드와 연동되는 부분)
    # OpenCR 코드는 command.equals("1")일 때 모터를 움직이고 LED를 끕니다.
    print("OpenCR 보드에 '1\\n' 신호를 보내 모터를 움직이고 LED를 끕니다.")
    ser_opencr.write('1\n'.encode('utf-8'))
    time.sleep(4) # OpenCR 코드의 delay(3000)보다 길게 대기

    # OpenCR 코드는 command.equals("0")일 때 모터를 원위치하고 LED를 켭니다.
    print("OpenCR 보드에 '0\\n' 신호를 보내 모터를 원위치하고 LED를 켭니다.")
    ser_opencr.write('0\n'.encode('utf-8'))
    time.sleep(4) # OpenCR 코드의 delay(3000)보다 길게 대기

    print("테스트 완료.")

except serial.SerialException as se:
    print(f"시리얼 통신 오류가 발생했습니다: {se}")
    print("1. 시리얼 포트 이름이 올바른지 확인하세요. (예: /dev/ttyACM0)")
    print("2. 보드에 전원이 들어와 있는지, 컴퓨터와 잘 연결되어 있는지 확인하세요.")
    print("3. 'sudo chmod 666 [포트이름]' 와 같이 권한을 부여했는지 확인하세요.")

except Exception as e:
    print(f"예상치 못한 오류가 발생했습니다: {e}")

finally:
    # 7. 프로그램 종료 시 반드시 모든 장치를 정지하고 연결을 종료
    print("안전을 위해 로봇을 정지시키고 연결을 종료합니다.")
    if bot is not None:
        bot.set_car_motion(0.0, 0.0, 0.0)
        print("Rosmaster 연결을 종료했습니다.")
   
    if ser_opencr is not None and ser_opencr.is_open:
        ser_opencr.close()
        print("OpenCR 연결을 종료했습니다.")
