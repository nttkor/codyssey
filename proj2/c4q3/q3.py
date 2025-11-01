import os  # 운영체제 기능을 사용하기 위한 모듈
import random  # 센서 데이터를 무작위로 생성하기 위한 모듈
import threading  # 멀티 쓰레드를 구현하기 위한 모듈
import time  # 시간 지연 및 주기 제어를 위한 모듈
import sqlite3  # SQLite 데이터베이스를 사용하기 위한 모듈
from datetime import datetime  # 현재 시간 정보를 얻기 위한 모듈

import matplotlib  # matplotlib 백엔드 설정용
matplotlib.use('Agg')  # GUI 없이 이미지 저장만 가능하게 설정
import matplotlib.pyplot as plt  # 그래프를 그리기 위한 모듈

os.chdir(os.path.dirname(__file__))  # 현재 파일 위치로 작업 디렉토리 변경

class Node:  # 큐의 노드 클래스 정의
    def __init__(self, data):  # 노드 초기화
        self.data = data  # 저장할 데이터
        self.next = None  # 다음 노드 참조

# 센서 데이터를 안전하게 저장하고 꺼내기 위한 FIFO 큐입니다.
# 멀티 쓰레드 환경에서도 동기화를 위해 threading.Lock()을 사용합니다.
class NodeQueue:  # 노드 기반 FIFO 큐 클래스 정의
    def __init__(self):  # 큐 초기화
        self.front = None  # 큐의 앞쪽 노드
        self.rear = None  # 큐의 뒤쪽 노드
        self.lock = threading.Lock()  # 멀티 쓰레드 안전을 위한 락

    def put(self, data):  # 큐에 데이터 추가
        new_node = Node(data)  # 새 노드 생성
        with self.lock:  # 락을 걸고 작업
            if self.rear is None:  # 큐가 비어있을 경우
                self.front = self.rear = new_node  # front와 rear 모두 새 노드로 설정
            else:
                self.rear.next = new_node  # 기존 rear 뒤에 새 노드 연결
                self.rear = new_node  # rear를 새 노드로 갱신

    def get(self):  # 큐에서 데이터 꺼내기
        with self.lock:  # 락을 걸고 작업
            if self.front is None:  # 큐가 비어있으면 None 반환
                return None
            data = self.front.data  # front의 데이터 저장
            self.front = self.front.next  # front를 다음 노드로 이동
            if self.front is None:  # 큐가 비어있으면 rear도 초기화
                self.rear = None
            return data  # 꺼낸 데이터 반환

    def is_empty(self):  # 큐가 비어있는지 확인
        with self.lock:
            return self.front is None  # front가 None이면 비어있음

sensorQ = NodeQueue()  # 센서 데이터를 저장할 큐 인스턴스 생성

class ParmSensor:  # 센서 클래스 정의
    def __init__(self, name):  # 센서 초기화
        self.name = name  # 센서 이름
        self.temperature = 0  # 온도 초기값
        self.light = 0  # 조도 초기값
        self.humidity = 0  # 습도 초기값

    def SetData(self):  # 센서 데이터를 무작위로 설정
        self.temperature = random.randint(20, 30)  # 온도: 20~30 사이
        self.light = random.randint(5000, 10000)  # 조도: 5000~10000 사이
        self.humidity = random.randint(40, 95)  # 습도: 40~95 사이

    def GetData(self):  # 센서 데이터를 반환
        return self.temperature, self.light, self.humidity  # 튜플로 반환
    
# SQLite를 사용하여 parm_data 테이블에 센서 데이터를 저장합니다.
# insert_sensor_data()로 삽입하고, get_sensor_data()로 조회합니다.
def insert_sensor_data(sensor_name, temperature, light, humidity):  # 센서 데이터를 DB에 저장
    conn = sqlite3.connect("smartfarm.db")  # DB 연결
    cursor = conn.cursor()  # 커서 생성
    # 데이터 삽입 SQL 실행
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ✅ 문자열로 변환
    cursor.execute("""  
        INSERT INTO parm_data (sensor_name, timestamp, temperature, light, humidity)
        VALUES (?, ?, ?, ?, ?)
    """, (sensor_name, timestamp, temperature, light, humidity))  # 현재 시간 포함 삽입
    conn.commit()  # 변경사항 저장
    conn.close()  # 연결 종료


def get_sensor_data():  # DB에서 센서 데이터를 조회
    conn = sqlite3.connect("smartfarm.db")  # DB 연결
    cursor = conn.cursor()  # 커서 생성
    cursor.execute("SELECT sensor_name, timestamp, temperature, humidity FROM parm_data")  # 데이터 조회
    rows = cursor.fetchall()  # 결과 가져오기
    conn.close()  # 연결 종료
    return rows  # 조회된 데이터 반환

RED = "\033[91m"  # 빨간색 ANSI 코드
RESET = "\033[0m"  # 색상 초기화 코드


# 각 센서가 2초마다 데이터를 생성하고 큐에 넣습니다.
def sensor_worker(sensor, stop_event):  # 센서 쓰레드 함수
    while not stop_event.is_set():  # 종료 이벤트가 설정되지 않은 동안 반복
        sensor.SetData()  # 센서 데이터 설정
        temp, light, humi = sensor.GetData()  # 센서 데이터 가져오기
        sensorQ.put((sensor.name, temp, light, humi))  # 큐에 데이터 저장
                # 습도 90 이상일 때 빨간색으로 출력
        if humi >= 90:
            print(f"{RED}[센서] {sensor.name} → temp:{temp}, light:{light}, humi:{humi}{RESET}")
        else:
            print(f"[센서] {sensor.name} → temp:{temp}, light:{light}, humi:{humi}")

        time.sleep(2)

# 큐에서 데이터를 꺼내 DB에 저장합니다.
def db_worker(stop_event):  # DB 쓰레드 함수
    while not stop_event.is_set():  # 종료 이벤트가 설정되지 않은 동안 반복
        data = sensorQ.get()  # 큐에서 데이터 꺼내기
        if data:  # 데이터가 있으면
            sensor_name, temp, light, humi = data  # 데이터 분해
            insert_sensor_data(sensor_name, temp, light, humi)  # DB에 저장
            print(f"[DB] 저장됨 → {sensor_name}, temp:{temp}, light:{light}, humi:{humi}")  # 콘솔 출력
        time.sleep(0.1)  # 1초 대기

# 시간대별 평균 온도를 센서별로 선 그래프로 표시합니다.
# 습도가 90 이상인 시간대는 빨간색 선으로 강조합니다.
# 결과는 sensor_plot.png로 저장됩니다.
def plot_sensor_data():  # 그래프 시각화 함수
    data = get_sensor_data()  # DB에서 데이터 조회
    if not data:  # 데이터가 없으면 종료
        print("데이터가 없습니다.")
        return

    grouped = {}  # 센서별 시간대별 온도 저장용 딕셔너리
    high_humi_hours = set()  # 습도 90 이상인 시간대 저장용 집합

    for name, ts, temp, humi in data:  # 조회된 데이터 반복
        hour = int(ts[11:13])  # 시간 추출 (HH)
        grouped.setdefault(name, {}).setdefault(hour, []).append(temp)  # 온도 저장
        if humi >= 90:  # 습도 90 이상이면
            high_humi_hours.add((name, hour))  # 해당 센서와 시간 저장

    plt.figure(figsize=(10, 6))  # 그래프 크기 설정
    for name, hour_dict in grouped.items():  # 센서별 반복
        hours = sorted(hour_dict.keys())  # 시간 정렬
        avg_temps = [sum(hour_dict[h]) / len(hour_dict[h]) for h in hours]  # 평균 온도 계산
        for i in range(len(hours) - 1):  # 선 그래프 그리기
            h1, h2 = hours[i], hours[i + 1]  # 두 시간대
            t1, t2 = avg_temps[i], avg_temps[i + 1]  # 두 시간대의 평균 온도
            color = 'red' if (name, h1) in high_humi_hours or (name, h2) in high_humi_hours else 'blue'  # 색상 결정
            plt.plot([h1, h2], [t1, t2], color=color)  # 선 그리기
        plt.scatter(hours, avg_temps, label=name)  # 점 찍기

    plt.xlabel("Hour of Day")  # x축 라벨
    plt.ylabel("Average Temperature")  # y축 라벨
    plt.title("Sensor-wise Hourly Average Temperature")  # 그래프 제목
    plt.legend()  # 범례 표시
    plt.grid(True)  # 격자 표시
    plt.tight_layout()  # 레이아웃 정리
    plt.savefig("sensor_plot.png")  # 그래프를 이미지 파일로 저장
    print("📊 그래프가 sensor_plot.png 파일로 저장되었습니다.")  # 저장 완료 메시지

# 메인 함수
# 실행 흐름 요약
# 센서 객체 5개 생성 (Parm-1 ~ Parm-5)
# 각 센서에 대해 쓰레드 실행 → 센서 데이터 생성 및 큐에 저장
# DB 쓰레드 실행 → 큐에서 데이터 꺼내 DB에 저장
# 사용자 입력으로 'q'를 입력하면 모든 쓰레드 종료
# 종료 후 DB 데이터를 기반으로 그래프 생성 및 저장
def main():  # 프로그램의 시작점 정의
    stop_event = threading.Event()  # 쓰레드 종료를 제어할 이벤트 객체 생성

    sensors = [ParmSensor(f"Parm-{i}") for i in range(1, 6)]  # ParmSensor 객체 5개 생성 (이름: Parm-1 ~ Parm-5)
    threads = []  # 쓰레드들을 저장할 리스트 초기화

    for sensor in sensors:  # 각 센서에 대해 반복
        t = threading.Thread(target=sensor_worker, args=(sensor, stop_event))  # 센서 쓰레드 생성
        t.start()  # 쓰레드 시작
        threads.append(t)  # 쓰레드 리스트에 추가

    db_thread = threading.Thread(target=db_worker, args=(stop_event,))  # DB 쓰레드 생성
    db_thread.start()  # DB 쓰레드 시작
    threads.append(db_thread)  # 쓰레드 리스트에 추가

    print("센서 모니터링 중... 종료하려면 'q'를 입력하세요.")  # 사용자에게 종료 방법 안내
    user_input = input()  # 사용자 입력 받기
    stop_event.set()  # 모든 쓰레드에 종료 신호 전달
    # while True:  # 사용자 입력을 기다리는 루프
    #     user_input = input()  # 사용자 입력 받기
    #     if user_input.strip().lower() == 'q':  # 입력이 'q'이면 종료 조건 만족
    #         stop_event.set()  # 모든 쓰레드에 종료 신호 전달
    #         break  # 루프 종료

    for t in threads:  # 모든 쓰레드에 대해 반복
        t.join()  # 쓰레드가 종료될 때까지 대기

    print("모든 쓰레드 종료됨. 그래프를 출력합니다.")  # 종료 메시지 출력
    plot_sensor_data()  # 센서 데이터 시각화 함수 호출

# 프로그램이 직접 실행될 경우 main() 함수 호출
if __name__ == '__main__':  # 이 파일이 직접 실행될 경우
    main()  # main 함수 실행
