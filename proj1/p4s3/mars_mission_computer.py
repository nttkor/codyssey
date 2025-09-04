import json
import time
import threading
import multiprocessing
import platform
import psutil
from datetime import datetime
import random
import sys
import os

# ===============================
# [1] 더미 센서 클래스 정의
# ===============================
class DummySensor:
    def __init__(self):
        # 센서 측정값 딕셔너리 초기화
        self.env_values = {
            "mars_base_internal_temperature": 0.0,
            "mars_base_external_temperature": 0.0,
            "mars_base_internal_humidity": 0.0,
            "mars_base_external_illuminance": 0.0,
            "mars_base_internal_co2": 0.0,
            "mars_base_internal_oxygen": 0.0
        }

    # 랜덤값으로 환경 데이터 설정
    def set_env(self):
        self.env_values["mars_base_internal_temperature"] = round(random.uniform(18, 30), 2)
        self.env_values["mars_base_external_temperature"] = round(random.uniform(0, 21), 2)
        self.env_values["mars_base_internal_humidity"] = round(random.uniform(50, 60), 2)
        self.env_values["mars_base_external_illuminance"] = round(random.uniform(500, 715), 2)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 4)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    # 환경 값 반환
    def get_env(self):
        # 보너스: 로그 파일로 저장
        log_line = f"{datetime.now()} | " + " | ".join([f"{k}: {v}" for k, v in self.env_values.items()])
        with open("sensor_log.txt", "a") as log_file:
            log_file.write(log_line + "\n")
        return self.env_values


# ===============================
# [2] 미션 컴퓨터 클래스 정의
# ===============================
class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()
        self.env_values = {}
        self.running = multiprocessing.Event()
        self.running.set()

        # 출력 항목 설정 (setting.txt로부터 로드)
        self.setting = {
            "os": True,
            "os_version": True,
            "cpu_type": True,
            "cpu_cores": True,
            "memory_total_MB": True,
            "cpu_usage_percent": True,
            "memory_usage_percent": True
        }
        self.load_setting()

    # setting.txt에서 사용자 설정 로드
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

    # 20초에 한 번 시스템 정보 출력
    def get_mission_computer_info(self):
        while self.running.is_set():
            try:
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
            except Exception as e:
                print(f"[에러] 시스템 정보 수집 중 오류 발생: {e}")
                break

    # 20초에 한 번 시스템 부하 출력
    def get_mission_computer_load(self):
        while self.running.is_set():
            try:
                load_sources = {
                    "cpu_usage_percent": lambda: psutil.cpu_percent(interval=1),
                    "memory_usage_percent": lambda: psutil.virtual_memory().percent
                }
                load = {k: getter() for k, getter in load_sources.items() if self.setting[k]}
                print("[System Load - JSON 출력]")
                print(json.dumps(load, indent=4))
                time.sleep(20)
            except Exception as e:
                print(f"[에러] 시스템 부하 수집 중 오류 발생: {e}")
                break

    # 5초에 한 번 센서 데이터 출력
    def get_sensor_data(self):
        while self.running.is_set():
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            print("[Sensor Data - JSON 출력]")
            print(json.dumps(self.env_values, indent=4))
            time.sleep(5)

    # 종료 함수
    def stop(self):
        self.running.clear()
        print("System stopped...")


# ===============================
# [3] 사용자 키 입력으로 종료 제어
# ===============================
def wait_for_key(mc_list):
    while any(mc.running.is_set() for mc in mc_list):
        key = input("종료하려면 'q'를 입력하세요: ")
        if key.lower() == 'q':
            for mc in mc_list:
                mc.stop()
            break


# ===============================
# [4] 멀티스레드 실행 함수
# ===============================
def run_threads(mc):
    threads = [
        threading.Thread(target=mc.get_mission_computer_info),
        threading.Thread(target=mc.get_mission_computer_load),
        threading.Thread(target=mc.get_sensor_data)
    ]

    for t in threads:
        t.daemon = True
        t.start()

    input_thread = threading.Thread(target=wait_for_key, args=([mc],))
    input_thread.daemon = True
    input_thread.start()

    for t in threads:
        t.join()


# ===============================
# [5] 멀티프로세스 실행 함수
# ===============================
def run_processes():
    # 문제 요구사항에 따라 명시적 이름 부여
    runComputer1 = MissionComputer()
    runComputer2 = MissionComputer()
    runComputer3 = MissionComputer()

    processes = [
        multiprocessing.Process(target=runComputer1.get_mission_computer_info),
        multiprocessing.Process(target=runComputer2.get_mission_computer_load),
        multiprocessing.Process(target=runComputer3.get_sensor_data),
    ]

    for p in processes:
        p.start()

    # 입력 대기 프로세스
    input_process = multiprocessing.Process(
        target=wait_for_key, args=([runComputer1, runComputer2, runComputer3],)
    )
    input_process.start()

    input_process.join()

    # 모든 프로세스 종료
    for p in processes:
        p.terminate()
    for p in processes:
        p.join()

    print("모든 프로세스 종료 완료.")


# ===============================
# [6] 메인 실행부
# ===============================
if __name__ == "__main__":
    # 작업 디렉토리 설정 (필요 시 수정)
    os.chdir('/home/mpeg4/Codyssey/proj1/p4s3')

    # [1단계] 멀티스레드 실행
    print("== 멀티스레드 실행 시작 ==")
    runComputer = MissionComputer()
    run_threads(runComputer)

    # [2단계] 멀티프로세스 실행
    print("\n== 멀티프로세스 실행 시작 ==")
    run_processes()
