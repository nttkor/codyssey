# mars_mission_computer.py

import os
import random
import datetime
import json
import time
import threading
import statistics

class DummySensor:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": 0.0,
            "mars_base_external_temperature": 0.0,
            "mars_base_internal_humidity": 0.0,
            "mars_base_external_illuminance": 0.0,
            "mars_base_internal_co2": 0.0,
            "mars_base_internal_oxygen": 0.0
        }

    def set_env(self):
        self.env_values["mars_base_internal_temperature"] = round(random.uniform(18, 30), 2)
        self.env_values["mars_base_external_temperature"] = round(random.uniform(0, 21), 2)
        self.env_values["mars_base_internal_humidity"] = round(random.uniform(50, 60), 2)
        self.env_values["mars_base_external_illuminance"] = round(random.uniform(500, 715), 2)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 4)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    def get_env(self):
        return self.env_values

    def save_log(self):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = (
            f"{timestamp}, "
            f"내부 온도: {self.env_values['mars_base_internal_temperature']}°C, "
            f"외부 온도: {self.env_values['mars_base_external_temperature']}°C, "
            f"내부 습도: {self.env_values['mars_base_internal_humidity']}%, "
            f"외부 광량: {self.env_values['mars_base_external_illuminance']} W/m², "
            f"내부 CO2: {self.env_values['mars_base_internal_co2']}%, "
            f"내부 O2: {self.env_values['mars_base_internal_oxygen']}%\n"
        )
        with open("environment_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)


class MissionComputer:
    
    def __init__(self):
        self.env_values = {}  # 화성 기지의 환경에 대한 값을 저장할 수 있는 딕서너리 객체
        self.ds = DummySensor()
        self.running = True
        self.data_buffer = []  # 5분 평균용

    def get_sensor_data(self):
        start_time = time.time()
        while self.running:
            self.ds.set_env()
            env_data = self.ds.get_env()
            self.env_values = env_data.copy()

            # 저장
            self.ds.save_log()

            # 버퍼에 데이터 추가
            self.data_buffer.append(env_data)
            if len(self.data_buffer) > 60:  # 5분(5*60=300초, 5초마다 수집이므로 60개)
                self.data_buffer.pop(0)

            # JSON 형태로 출력
            json_output = json.dumps(self.env_values, indent=4, ensure_ascii=False)
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 환경 데이터:")
            print(json_output)

            # 5분 평균 출력 (60개 수집 시마다)
            if int(time.time() - start_time) % 300 < 5 and len(self.data_buffer) == 60:
                self.print_5min_average()

            time.sleep(5)

        print("System stopped...")

    def print_5min_average(self):
        print("\n--- 5분 평균 환경 값 ---")
        avg_values = {}
        keys = self.data_buffer[0].keys()
        for key in keys:
            values = [data[key] for data in self.data_buffer]
            avg_values[key] = round(statistics.mean(values), 2)
        print(json.dumps(avg_values, indent=4, ensure_ascii=False))
        print("------------------------\n")

    def stop(self):
        self.running = False


# 입력 감지 쓰레드
def wait_for_key(mc):
    while mc.running:
        key = input("종료하려면 'q'를 입력하세요: ")
        if key.lower() == 'q':
            mc.stop()


if __name__ == "__main__":
    os.chdir('/home/mpeg4/Codyssey/proj1/p4s3')

    # 미션 컴퓨터 인스턴스
    RunComputer = MissionComputer()

    # 키 입력 감지 쓰레드 시작
    input_thread = threading.Thread(target=wait_for_key, args=(RunComputer,))
    input_thread.daemon = True
    input_thread.start()

    # 센서 데이터 수집 시작
    RunComputer.get_sensor_data()
