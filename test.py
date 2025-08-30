import serial
import time

# 라즈베리파이의 하드웨어 시리얼 포트 이름
# 최신 라즈베리파이 OS에서는 /dev/serial0이 표준입니다.
# 만약 작동하지 않으면 /dev/ttyAMA0으로 시도해보세요.
SERIAL_PORT = '/dev/serial0' 
BAUD_RATE = 9600 # OpenCR(아두이노)의 Serial.begin()에 설정된 값과 일치해야 합니다.

try:
    # 시리얼 포트 열기
    opencr = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1.0)
    print(f"'{SERIAL_PORT}' 포트 연결 성공. 2초 후 테스트 시작...")
    time.sleep(2) # 보드가 리셋되고 안정화될 시간을 줍니다.

    # 2초마다 그리퍼 닫기('1')와 열기('0')를 반복
    while True:
        # 그리퍼 닫기 명령 전송
        print("명령 '1' 전송 (그리퍼 닫기)")
        opencr.write(b'1') # 데이터를 바이트 형태로 전송합니다.
        time.sleep(2)

        # 그리퍼 열기 명령 전송
        print("명령 '0' 전송 (그리퍼 열기)")
        opencr.write(b'0')
        time.sleep(2)

except serial.SerialException as e:
    print(f"시리얼 포트 오류: {e}")
    print("1. 'sudo raspi-config'에서 시리얼 포트가 활성화되었는지 확인하세요.")
    print("2. 'sudo usermod -a -G dialout <사용자이름>'으로 권한을 부여했는지 확인하세요.")
    print("3. TX, RX, GND 연결이 올바른지 확인하세요.")

except KeyboardInterrupt:
    print("\n프로그램 종료. 포트를 닫습니다.")

finally:
    if 'opencr' in locals() and opencr.is_open:
        opencr.close()
