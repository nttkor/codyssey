import os  # 운영체제 관련 기능을 사용하기 위한 모듈
import random  # 센서 데이터를 무작위로 생성하기 위한 모듈
import threading  # 센서 쓰레드를 만들기 위한 모듈
import time  # 시간 지연 및 타이밍 제어를 위한 모듈
import sqlite3  # SQLite 데이터베이스를 사용하기 위한 모듈
from datetime import datetime  # 현재 시간을 얻기 위한 모듈

os.chdir(os.path.dirname(__file__))  # 현재 파일 위치로 작업 디렉토리 변경

RED = "\033[91m"  # 콘솔 출력 시 빨간색 ANSI 코드
RESET = "\033[0m"  # 콘솔 출력 색상 초기화 코드

class ParmSensor:  # 센서 클래스 정의
    def __init__(self, name):  # 센서 객체 초기화
        self.name = name  # 센서 이름 저장
        self.temperature = 0  # 온도 초기값
        self.light = 0  # 조도 초기값
        self.humidity = 0  # 습도 초기값

    def SetData(self):  # 센서 데이터를 무작위로 설정
        self.temperature = random.randint(20, 30)  # 온도: 20~30 사이
        self.light = random.randint(5000, 10000)  # 조도: 5000~10000 사이
        self.humidity = random.randint(40, 95)  # 습도: 40~95 사이

    def GetData(self):  # 센서 데이터를 반환
        return self.temperature, self.light, self.humidity  # 온도, 조도, 습도 반환

def insert_sensor_data(sensor_name, temperature, light, humidity):  # 센서 데이터를 DB에 저장
    conn = sqlite3.connect("smartfarm.db")  # 데이터베이스 연결
    cursor = conn.cursor()  # 커서 객체 생성
    cursor.execute("""  # 데이터 삽입 SQL 실행
        INSERT INTO parm_data (sensor_name, timestamp, temperature, light, humidity)
        VALUES (?, ?, ?, ?, ?)
    """, (sensor_name, datetime.now(), temperature, light, humidity))  # 현재 시간 포함 데이터 삽입
    conn.commit()  # 변경사항 커밋
    conn.close()  # 연결 종료

def sensor_worker(sensor, stop_event):  # 센서 쓰레드 함수
    while not stop_event.is_set():  # 종료 이벤트가 설정되지 않은 동안 반복
        sensor.SetData()  # 센서 데이터 설정
        temp, light, humi = sensor.GetData()  # 센서 데이터 가져오기
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 시간 문자열로 저장

        insert_sensor_data(sensor.name, temp, light, humi)  # 데이터베이스에 저장

        if humi > 90:  # 습도가 90 초과일 경우
            print(f"{timestamp} {sensor.name} — temp {temp}, light {light}, humi {RED}{humi}{RESET}")  # 빨간색으로 출력
        else:  # 습도가 90 이하일 경우
            print(f"{timestamp} {sensor.name} — temp {temp}, light {light}, humi {humi}")  # 일반 출력

        for _ in range(10):  # 10초 동안 1초씩 나눠서 대기
            if stop_event.is_set():  # 종료 이벤트 확인
                break  # 종료 이벤트가 설정되면 루프 탈출
            time.sleep(1)  # 1초 대기

def main():  # 프로그램 시작 함수
    stop_event = threading.Event()  # 종료 이벤트 객체 생성
    sensors = [ParmSensor(f"Parm-{i}") for i in range(1, 6)]  # 센서 객체 5개 생성
    threads = []  # 쓰레드 리스트 초기화

    for sensor in sensors:  # 각 센서에 대해
        thread = threading.Thread(target=sensor_worker, args=(sensor, stop_event))  # 쓰레드 생성
        thread.start()  # 쓰레드 시작
        threads.append(thread)  # 쓰레드 리스트에 추가

    print("센서 모니터링 중... 종료하려면 'q'를 입력하세요.")  # 사용자 안내 메시지 출력

    while True:  # 사용자 입력 대기 루프
        user_input = input()  # 사용자 입력 받기
        if user_input.strip().lower() == 'q':  # 입력이 'q'이면
            print("종료 중...")  # 종료 메시지 출력
            stop_event.set()  # 종료 이벤트 설정
            break  # 루프 탈출

    for thread in threads:  # 모든 쓰레드에 대해
        thread.join()  # 쓰레드 종료 대기

    print("모든 센서 쓰레드가 종료되었습니다.")  # 종료 완료 메시지 출력

if __name__ == '__main__':  # 이 파일이 직접 실행될 경우
    main()  # main 함수 실행
