'''
📁 보너스 과제 (선택 설정 파일 setting.txt 예시)

추가 요구가 있을 경우 이 파일을 이용해서 출력 항목을 제어할 수 있도록 확장 가능:

show_os=true
show_cpu=true
show_memory=true
'''
import os
import json
import time
import threading
import platform
import psutil  # 시스템 정보 및 리소스 사용량
from datetime import datetime
import random

# DummySensor는 기존 과제 1 내용 기반
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


# 개선된 MissionComputer 클래스
class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()
        self.env_values = {}
        self.running = True

    def get_sensor_data(self):
        while self.running:
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            print("[Sensor Data - JSON 출력]")
            print(json.dumps(self.env_values, indent=4))
            time.sleep(5)

    def stop(self):
        self.running = False
        print("System stopped...")

    def get_mission_computer_info(self):
        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "cpu_type": platform.processor(),
            "cpu_cores": psutil.cpu_count(logical=False),
            "memory_total_MB": round(psutil.virtual_memory().total / (1024 * 1024), 2)
        }
        print("[System Info - JSON 출력]")
        print(json.dumps(info, indent=4))
        return info

    def get_mission_computer_load(self):
        load = {
            "cpu_usage_percent": psutil.cpu_percent(interval=1),
            "memory_usage_percent": psutil.virtual_memory().percent
        }
        print("[System Load - JSON 출력]")
        print(json.dumps(load, indent=4))
        return load


# 사용자 키 입력 스레드 함수
def wait_for_key(mc):
    while mc.running:
        key = input("종료하려면 'q'를 입력하세요: ")
        if key.lower() == 'q':
            mc.stop()


# 실행 블록
if __name__ == "__main__":
    # 실행 경로 설정 (환경에 따라 수정 가능)
    os.chdir('/home/mpeg4/Codyssey/proj1/p4s3')

    # 인스턴스 생성
    runComputer = MissionComputer()

    # 시스템 정보 출력
    runComputer.get_mission_computer_info()

    # 시스템 부하 출력
    runComputer.get_mission_computer_load()

    # 센서 감시 시작 (스레드에서 키 입력 감시)
    input_thread = threading.Thread(target=wait_for_key, args=(runComputer,))
    input_thread.daemon = True
    input_thread.start()

    # 센서 데이터 지속 수집
    runComputer.get_sensor_data()
