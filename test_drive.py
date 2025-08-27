#!/usr/bin/env python3
import time
from rosmaster import Rosmaster   # rosmaster.py와 같은 폴더에 있을 때

PORT = "/dev/ttyUSB2"   # 필요시 "/dev/ttyACM0"나 /dev/serial/by-id/... 로 교체
CAR_TYPE = 1            # X3 = 1

def main():
    bot = Rosmaster(com=PORT, debug=True)
    bot.create_receive_threading()
    time.sleep(0.1)

    # 통신 확인
    ver = bot.get_version()
    print("FW version:", ver)
    bot.set_beep(50)                   # 50ms 삑

    # 차종 설정(한 번만 해도 됨)
    bot.set_car_type(CAR_TYPE)
    time.sleep(0.1)

    # 천천히 1초 전진 후 정지
    bot.set_car_motion(0.2, 0.0, 0.0)  # vx=0.2 m/s, vy=0, yaw=0
    time.sleep(1.0)
    bot.set_car_motion(0.0, 0.0, 0.0)

    # 상태 읽기 예시
    vx, vy, vz = bot.get_motion_data()
    print("motion:", vx, vy, vz)
    print("battery[V]:", bot.get_battery_voltage())

if __name__ == "__main__":
    main()
