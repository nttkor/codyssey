import os
import json
import time
import threading
import multiprocessing
import platform
import psutil
from datetime import datetime
import random
import sys

# 센서 값을 생성하는 더미 클래스
class DummySensor:
    def __init__(self):
        # 초기 센서 데이터
        self.env_values = {
            "mars_base_internal_temperature": 0.0,
            "mars_base_external_temperature": 0.0,
            "mars_base_internal_humidity": 0.0,
            "mars_base_external_illuminance": 0.0,
            "mars_base_internal_co2": 0.0,
            "mars_base_internal_oxygen": 0.0
        }

    # 무작위 환경 데이터 생성
    def set_env(self):
        self.env_values["mars_base_internal_temperature"] = round(random.uniform(18, 30), 2)
        self.env_values["mars_base_external_temperature"] = round(random.uniform(0, 21), 2)
        self.env_values["mars_base_internal_humidity"] = round(random.uniform(50, 60), 2)
        self.env_values["mars_base_external_illuminance"] = round(random.uniform(500, 715), 2)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 4)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    # 현재 센서 데이터 반환
    def get_env(self):
        return self.env_values


# 메인 미션 컴퓨터 클래스
class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()
        self.env_values = {}
        self.running = multiprocessing.Event()  # 종료 제어용 Event 객체
        self.running.set()  # 기본적으로 실행 상태

        # 출력할 항목 설정
        self.setting = {
            "os": True,
            "os_version": True,
            "cpu_type": True,
            "cpu_cores": True,
            "memory_total_MB": True,
            "cpu_usage_percent": True,
            "memory_usage_percent": True
        }
        self.load_setting()  # setting.txt 로드

    # 설정 파일 로드
    def load_setting(self):
        setting_file = "setting.txt"
        try:
            with open(setting_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or '=' not in line:
                        continue
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().lower()
                    if key in self.setting:
                        self.setting[key] = (value == 'true')
        except FileNotFoundError:
            print(f"[경고] '{setting_file}' 파일을 찾을 수 없습니다. 기본 설정을 사용합니다.")
        except Exception as e:
            print(f"[에러] 설정 파일을 읽는 중 오류 발생: {e}. 기본 설정을 사용합니다.")

    # 시스템 정보 출력 (20초 간격)
    def get_mission_computer_info(self):
        while self.running.is_set():
            info_sources = {
                "os": lambda: platform.system(),
                "os_version": lambda: platform.version(),
                "cpu_type": lambda: platform.processor(),
                "cpu_cores": lambda: psutil.cpu_count(logical=False),
                "memory_total_MB": lambda: round(psutil.virtual_memory().total / (1024 * 1024), 2)
            }
            info = {k: getter() for k, getter in info_sources.items() if self.setting[k]}
            print("[System Info - JSON 출력]")
            print(json.dumps(info, indent=4))
            time.sleep(20)

    # 시스템 부하 정보 출력 (20초 간격)
    def get_mission_computer_load(self):
        while self.running.is_set():
            load_sources = {
                "cpu_usage_percent": lambda: psutil.cpu_percent(interval=1),
                "memory_usage_percent": lambda: psutil.virtual_memory().percent
            }
            load = {k: getter() for k, getter in load_sources.items() if self.setting[k]}
            print("[System Load - JSON 출력]")
            print(json.dumps(load, indent=4))
            time.sleep(20)

    # 센서 데이터 출력 (5초 간격)
    def get_sensor_data(self):
        while self.running.is_set():
            self.ds.set_env()  # 랜덤 데이터 생성
            self.env_values = self.ds.get_env()  # 데이터 저장
            print("[Sensor Data - JSON 출력]")
            print(json.dumps(self.env_values, indent=4))
            time.sleep(5)

    # 실행 중지 함수
    def stop(self):
        self.running.clear()
        print("System stopped...")


# 사용자의 키 입력을 기다리는 함수 ('q' 입력 시 종료)
def wait_for_key(mc_list):
    while any(mc.running.is_set() for mc in mc_list):
        key = input("종료하려면 'q'를 입력하세요: ")
        if key.lower() == 'q':
            for mc in mc_list:
                mc.stop()
            break


# --- 멀티스레드 실행 ---
def run_threads(mc):
    # 세 개의 메서드를 각각 스레드로 실행
    threads = [
        threading.Thread(target=mc.get_mission_computer_info),
        threading.Thread(target=mc.get_mission_computer_load),
        threading.Thread(target=mc.get_sensor_data)
    ]

    for t in threads:
        t.daemon = True  # 메인 스레드 종료 시 함께 종료
        t.start()

    # 키 입력 대기 스레드
    input_thread = threading.Thread(target=wait_for_key, args=([mc],))
    input_thread.daemon = True
    input_thread.start()

    # 각 스레드 종료 대기
    for t in threads:
        t.join()


# --- 멀티프로세스 실행 ---
def run_processes():
    # MissionComputer 인스턴스 3개 생성
    computers = [MissionComputer() for _ in range(3)]
    processes = []

    # 각 인스턴스에서 세 개의 메서드를 각각 프로세스로 실행
    for mc in computers:
        processes.append(multiprocessing.Process(target=mc.get_mission_computer_info))
        processes.append(multiprocessing.Process(target=mc.get_mission_computer_load))
        processes.append(multiprocessing.Process(target=mc.get_sensor_data))

    # 모든 프로세스 시작
    for p in processes:
        p.start()

    # 키 입력을 기다리는 별도 프로세스 실행
    input_process = multiprocessing.Process(target=wait_for_key, args=(computers,))
    input_process.start()

    # 키 입력 프로세스가 끝날 때까지 대기
    input_process.join()

    # 모든 실행 중인 프로세스 강제 종료
    for p in processes:
        p.terminate()

    for p in processes:
        p.join()

    print("모든 프로세스 종료 완료.")


# 메인 실행부
if __name__ == "__main__":
    os.chdir('/home/mpeg4/Codyssey/proj1/p4s3')  # 작업 디렉토리 설정

    # --- 1단계: 멀티스레드 실행 ---
    print("== 멀티스레드 실행 시작 ==")
    runComputer = MissionComputer()
    run_threads(runComputer)

    # --- 2단계: 멀티프로세스 실행 ---
    print("\n== 멀티프로세스 실행 시작 ==")
    run_processes()
