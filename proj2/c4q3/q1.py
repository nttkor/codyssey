import random                      # 랜덤 숫자 생성을 위한 모듈
import threading                   # 멀티 쓰레드 구현을 위한 모듈
import time                        # 시간 관련 함수 사용을 위한 모듈
from datetime import datetime      # 현재 시간 출력을 위한 모듈
import sys                         # 시스템 입력 처리를 위한 모듈

RED = "\033[91m"                   # 콘솔 출력용 빨간색 ANSI 코드
RESET = "\033[0m"                  # 콘솔 출력 색상 초기화 코드

# 센서 이름, 온도, 조도, 습도 속성을 가짐
# SetData()로 무작위 데이터 생성
# GetData()
class ParmSensor:                  # 스마트 팜 센서 클래스 정의
    def __init__(self, name):      # 생성자: 센서 이름 초기화
        self.name = name           # 센서 고유 이름
        self.temperature = 0       # 온도 초기값
        self.light = 0             # 조도 초기값
        self.humidity = 0          # 습도 초기값

    def SetData(self):             # 센서 데이터 생성 함수
        self.temperature = random.randint(20, 30)       # 온도: 20~30 사이 랜덤
        self.light = random.randint(5000, 10000)        # 조도: 5000~10000 사이 랜덤
        self.humidity = random.randint(40, 95)          # 습도: 40~95 사이 랜덤 (테스트용 확장)

    def GetData(self):             # 센서 데이터 반환 함수
        return self.temperature, self.light, self.humidity  # 온도, 조도, 습도 반환

# 각 센서가 10초 주기로 데이터를 생성
# 습도가 90% 초과 시 빨간색으로 출력
# stop_event가 설정되면 루프 종료
def sensor_worker(sensor, stop_event):                  # 센서 쓰레드 함수
    while not stop_event.is_set():                      # 종료 이벤트가 설정되지 않은 동안 반복
        sensor.SetData()                                # 센서 데이터 생성
        temp, light, humi = sensor.GetData()            # 센서 데이터 가져오기
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 시간 포맷팅

        if humi > 90:                                    # 습도가 90% 초과일 경우
            print(f"{timestamp} {sensor.name} — temp {temp}, light {light}, humi {RED}{humi}{RESET}")  # 빨간색 출력
        else:
            print(f"{timestamp} {sensor.name} — temp {temp}, light {light}, humi {humi}")              # 일반 출력
               # 10초를 1초씩 나눠서 체크
        for _ in range(10):
            if stop_event.is_set():
                break
            time.sleep(1)                                 # 10초 대기 후 반복

# 센서 5개 생성 (Parm-1 ~ Parm-5)
# 각 센서에 대해 쓰레드 실행
# 사용자 입력을 기다리며 'q' 입력 시 모든 쓰레드 종료
# 종료 후 메시지 출력
def main():                                              # 프로그램 실행 함수
    stop_event = threading.Event()                      # 종료 이벤트 생성
    sensors = [ParmSensor(f"Parm-{i}") for i in range(1, 6)]  # 센서 5개 생성
    threads = []                                         # 쓰레드 리스트 초기화

    for sensor in sensors:                              # 1q각 센서에 대해 쓰레드 시작
        thread = threading.Thread(target=sensor_worker, args=(sensor, stop_event))  # 쓰레드 생성
        thread.start()                                   # 쓰레드 시작
        threads.append(thread)                           # 쓰레드 리스트에 추가

    print("센서 모니터링 중... 종료하려면 'q'를 입력하세요.")  # 사용자 안내 메시지

    while True:                                          # 사용자 입력 대기 루프
        user_input = input()                             # 사용자 입력 받기
        if user_input.strip().lower() == 'q':            # 입력이 'q'일 경우
            print("종료 중...")                           # 종료 메시지 출력
            stop_event.set()                             # 종료 이벤트 설정
            break                                        # 루프 탈출

    for thread in threads:                               # 모든 쓰레드 종료 대기
        thread.join()                                    # 쓰레드 종료까지 대기

    print("모든 센서 쓰레드가 종료되었습니다.")             # 종료 완료 메시지 출력

if __name__ == '__main__':                               # 프로그램 시작점
    main()                                               # main() 함수 호출
