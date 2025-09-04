import os
import json
import time
import threading
import multiprocessing
import platform
import psutil
import random
from datetime import datetime

# ========== ✅ 반응형 슬립 함수 ==========
# 문제 4. 보너스 과제: 특정 키(q) 입력 시 즉시 멈출 수 있도록 구현
# 일반 time.sleep() 사용 시 sleep 중에는 종료 이벤트를 확인할 수 없음
# 따라서 interval 단위(기본 0.5초)로 stop_event를 반복 체크하면서 sleep 가능
# stop_event가 set되면 즉시 break 되어 루프나 쓰레드/프로세스 종료 가능
def responsive_sleep(duration, stop_event, interval=0.5):
    elapsed = 0
    while elapsed < duration:
        if stop_event.is_set():  # 종료 이벤트가 설정되었는지 체크
            break
        time.sleep(interval)     # interval 만큼 대기
        elapsed += interval      # 경과 시간 누적


# ========== ✅ 더미 센서 클래스 ==========
# 문제 1. 화성 기지 환경 데이터를 랜덤으로 생성하는 센서 시뮬레이션 클래스
# env_values 딕셔너리에 내부/외부 온도, 습도, 조도, CO2, 산소 농도 저장
class DummySensor:
    def __init__(self):
        # 초기값은 모두 0.0으로 세팅
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    # 문제 1. set_env(): 각 환경 값을 지정 범위 내에서 랜덤 생성
    # 시뮬레이션용이므로 실제 센서 값 대신 random 값 사용
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    # 문제 1. get_env(): 현재 환경 값 반환 및 로그 파일 기록
    # sensor_log.txt에 timestamp와 함께 기록
    # 반환은 copy()를 사용하여 외부에서 수정해도 원본 데이터 보존
    def get_env(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 현재 시간 문자열
        log_line = f'{timestamp}, ' + ', '.join(f'{v}' for v in self.env_values.values())
        # 로그 파일 append 모드로 저장
        with open('sensor_log.txt', 'a') as f:
            f.write(log_line + '\n')
        return self.env_values.copy()


# ========== ✅ 미션 컴퓨터 클래스 ==========
# 문제 2. MissionComputer 클래스
# 센서 데이터를 받아서 env_values에 저장하고, 출력
# 문제 3. 시스템 정보/부하 정보 수집 기능 추가
# 문제 4. 멀티스레드/멀티프로세스 대응 구조
class MissionComputer:
    def __init__(self, stop_event, name='MissionComputer'):
        self.name = name
        self.ds = DummySensor()          # DummySensor 인스턴스 생성
        self.env_values = {}             # 최신 센서 값 저장
        self.stop_event = stop_event     # 종료 이벤트 참조 (q 입력 시 루프 종료)
        self.sensor_history = []         # 5분 평균 계산용 히스토리 저장

        # 문제 3. setting.txt로 출력 항목 설정 가능
        self.setting = {
            'os': True,
            'os_version': True,
            'cpu_type': True,
            'cpu_cores': True,
            'memory_total_MB': True,
            'cpu_usage_percent': True,
            'memory_usage_percent': True
        }
        self.load_setting()  # setting.txt 파일 로드

    # 문제 3. setting.txt 읽어 출력 항목별 True/False로 반영
    # 파일이 없으면 기본값 사용
    def load_setting(self):
        try:
            with open('setting.txt', 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=')
                        self.setting[key.strip()] = value.strip().lower() == 'true'
        except FileNotFoundError:
            print('[경고] setting.txt 파일이 없어 기본 설정을 사용합니다.')

    # 문제 2. 센서 데이터 주기적 수집
    # 5초 간격으로 실행되며 stop_event가 set되면 종료
    # 5분(60회)마다 평균값 계산
    def get_sensor_data(self):
        while not self.stop_event.is_set():   # 종료 이벤트 체크
            self.ds.set_env()                  # 랜덤 환경값 생성
            self.env_values = self.ds.get_env()  # 환경값 저장 + 로그 기록
            self.sensor_history.append(self.env_values)
            # JSON 포맷으로 콘솔 출력
            print(f'[{self.name} - Sensor Data]')
            print(json.dumps(self.env_values, indent=4))

            # 보너스 과제: 5분 평균값 계산
            if len(self.sensor_history) >= 60:  # 60회 = 약 5분
                self.print_5min_average()
                self.sensor_history.clear()

            # 반복 간격: responsive_sleep으로 5초 동안 이벤트 체크
            responsive_sleep(5, self.stop_event)

    # 5분 평균값 계산 후 출력
    def print_5min_average(self):
        print(f'[{self.name} - 5분 평균]')
        avg = {}
        keys = self.sensor_history[0].keys()
        for key in keys:
            total = sum(sensor[key] for sensor in self.sensor_history)
            avg[key] = round(total / len(self.sensor_history), 4)
        print(json.dumps(avg, indent=4))

    # 문제 3. 시스템 정보 수집
    # 20초 간격으로 OS, CPU, 메모리 정보 수집 후 JSON 출력
    def get_mission_computer_info(self):
        while not self.stop_event.is_set():
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
            responsive_sleep(20, self.stop_event)

    # 문제 3. 실시간 CPU/메모리 부하 수집
    # 20초 간격으로 JSON 출력
    def get_mission_computer_load(self):
        while not self.stop_event.is_set():
            load_sources = {
                "cpu_usage_percent": lambda: psutil.cpu_percent(interval=1),
                "memory_usage_percent": lambda: psutil.virtual_memory().percent
            }
            load = {k: getter() for k, getter in load_sources.items() if self.setting[k]}
            print("[System Load - JSON 출력]")
            print(json.dumps(load, indent=4))
            responsive_sleep(20, self.stop_event)


# ========== ✅ 멀티쓰레드 실행 ==========
# 문제 4. 각 기능을 별도 쓰레드로 실행
# get_sensor_data, get_mission_computer_info, get_mission_computer_load
def run_threads(stop_event):
    mc = MissionComputer(stop_event, name='Thread-MC')
    # 각 기능별 쓰레드 생성
    threads = [
        threading.Thread(target=mc.get_sensor_data),
        threading.Thread(target=mc.get_mission_computer_info),
        threading.Thread(target=mc.get_mission_computer_load)
    ]
    # 쓰레드 시작
    for t in threads:
        t.start()
    # join은 현재 run_threads 내부에서만 적용됨, main 스레드는 영향 없음
    for t in threads:
        t.join()
    return threads



# ========== ✅ 멀티프로세스 실행 ==========
# 문제 4. 멀티프로세스 실행: MissionComputer 인스턴스를 3개 만들어 각각 실행
# get_sensor_data, get_mission_computer_info, get_mission_computer_load를 분리된 프로세스로 실행
def run_processes(stop_event):
    def proc_wrapper(target_func, name):
        def wrapper():
            mc = MissionComputer(stop_event, name)
            getattr(mc, target_func)()
        return wrapper
    target=proc_wrapper('get_sensor_data','Process-MC1')
    process_list = [
        multiprocessing.Process(target=proc_wrapper('get_sensor_data', 'Process-MC1'),daemon=True),
        multiprocessing.Process(target=proc_wrapper('get_mission_computer_info', 'Process-MC2'),daemon=True),
        multiprocessing.Process(target=proc_wrapper('get_mission_computer_load', 'Process-MC3'),daemon=True)
    ]
    for p in process_list:
        p.start()
    return process_list


# ========== ✅ 종료 대기 함수 ==========
# 문제 4. 보너스 과제: 멀티스레드/멀티프로세스 실행 중간에 q 입력 시 즉시 종료
# stop_event.set() 호출하여 모든 루프 중단
def wait_for_exit(stop_event):
    while not stop_event.is_set():
        try:
            key = input('종료하려면 q를 입력하세요: ').strip().lower()
            if key == 'q':
                stop_event.set()
        except KeyboardInterrupt:
            stop_event.set()


# ========== ✅ 메인 실행 ==========
if __name__ == '__main__':
    # 작업 경로를 현재 파일 경로로 고정 (log 파일이 같은 위치에 생성되도록)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    stop_event = multiprocessing.Event()  # 멀티프로세스, 멀티스레드 간 공유되는 종료 이벤트

    print('== 멀티프로세스 및 멀티스레드 실행 시작 ==')

    # 문제 4. 프로세스 실행
    processes = run_processes(stop_event)

    # 문제 4. 쓰레드 실행
    thread_runner = threading.Thread(target=run_threads, args=(stop_event,))
    thread_runner.start()

    # 종료 입력 대기 (q 입력 시 멈춤)
    wait_for_exit(stop_event)

    # 프로세스 종료 처리
    for p in processes:
        p.terminate()
    for p in processes:
        p.join()

    # 쓰레드 종료 대기
    thread_runner.join()

    print('== 모든 스레드 및 프로세스 종료 완료 ==')
