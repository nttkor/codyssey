'''
| 항목                            | 설명                      |
| ----------------------------- | ----------------------- |
| `get_sensor_data()`           | 5초마다 센서 정보 출력           |
| `get_mission_computer_info()` | 20초마다 시스템 정보 출력         |
| `get_mission_computer_load()` | 20초마다 시스템 부하 출력         |
| 멀티 스레드 실행                     | 하나의 인스턴스에서 3개 메소드 동시 실행 |
| 멀티 프로세스 실행                    | 각 메소드를 별도 프로세스로 실행      |
| 종료 처리                         | `q` 입력으로 스레드 또는 프로세스 종료 |

'''

import os
import json
import time
import threading
import multiprocessing
import platform
import psutil
import random
from datetime import datetime

# ----------------------
# DummySensor 정의
# ----------------------
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


# ----------------------
# MissionComputer 정의
# ----------------------
class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()
        self.running = True

    def stop(self):
        self.running = False
        print("System stopped...")

    def get_sensor_data(self):
        while self.running:
            self.ds.set_env()
            env = self.ds.get_env()
            print("[Sensor Data] 5초 주기 출력")
            print(json.dumps(env, indent=4))
            time.sleep(5)

    def get_mission_computer_info(self):
        while self.running:
            info = {
                "os": platform.system(),
                "os_version": platform.version(),
                "cpu_type": platform.processor(),
                "cpu_cores": psutil.cpu_count(logical=False),
                "memory_total_MB": round(psutil.virtual_memory().total / (1024 * 1024), 2)
            }
            print("[System Info] 20초 주기 출력")
            print(json.dumps(info, indent=4))
            time.sleep(20)

    def get_mission_computer_load(self):
        while self.running:
            load = {
                "cpu_usage_percent": psutil.cpu_percent(interval=1),
                "memory_usage_percent": psutil.virtual_memory().percent
            }
            print("[System Load] 20초 주기 출력")
            print(json.dumps(load, indent=4))
            time.sleep(20)


# ----------------------
# 스레드 입력 대기 (보너스 과제)
# ----------------------
def wait_for_key(mc):
    while mc.running:
        key = input("종료하려면 'q'를 입력하세요: ")
        if key.lower() == 'q':
            mc.stop()
            break


# ----------------------
# 멀티 스레드 실행
# ----------------------
def run_with_threads():
    mc = MissionComputer()

    threads = [
        threading.Thread(target=mc.get_sensor_data),
        threading.Thread(target=mc.get_mission_computer_info),
        threading.Thread(target=mc.get_mission_computer_load),
        threading.Thread(target=wait_for_key, args=(mc,))
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


# ----------------------
# 멀티 프로세스용 타겟 함수
# ----------------------
def run_info():
    mc = MissionComputer()
    mc.get_mission_computer_info()

def run_load():
    mc = MissionComputer()
    mc.get_mission_computer_load()

def run_sensor():
    mc = MissionComputer()
    mc.get_sensor_data()

# ----------------------
# 멀티 프로세스 종료 감시 (보너스 과제)
# ----------------------
def monitor_processes(processes):
    while True:
        key = input("프로세스를 종료하려면 'q'를 입력하세요: ")
        if key.lower() == 'q':
            for p in processes:
                p.terminate()
            print("All processes terminated.")
            break

# ----------------------
# 멀티 프로세스 실행
# ----------------------
def run_with_processes():
    p1 = multiprocessing.Process(target=run_info)
    p2 = multiprocessing.Process(target=run_load)
    p3 = multiprocessing.Process(target=run_sensor)

    p1.start()
    p2.start()
    p3.start()

    monitor_processes([p1, p2, p3])

    p1.join()
    p2.join()
    p3.join()


# ----------------------
# 메인
# ----------------------
if __name__ == "__main__":
    os.chdir('/home/mpeg4/Codyssey/proj1/p4s3')

    mode = input("실행 모드를 선택하세요 (1: 쓰레드 / 2: 프로세스): ")

    if mode == '1':
        run_with_threads()
    elif mode == '2':
        run_with_processes()
    else:
        print("잘못된 입력입니다.")