# mars_mission_computer.py

import random
import datetime

class DummySensor:
    def __init__(self):
        # 환경 정보 딕셔너리
        self.env_values = {
            "mars_base_internal_temperature": 0.0,
            "mars_base_external_temperature": 0.0,
            "mars_base_internal_humidity": 0.0,
            "mars_base_external_illuminance": 0.0,
            "mars_base_internal_co2": 0.0,
            "mars_base_internal_oxygen": 0.0
        }

    def set_env(self):
        '''
        DummySensor는 테스트를 위한 객체이므로 데이터를 랜덤으로 생성한다. 
        random.unifor()은 범위내의 실수를 반환한다. 
        round(num, ndigits)  ndigitis자리의  소수점을 반올림 한다. 
        '''
        self.env_values["mars_base_internal_temperature"] = round(random.uniform(18, 30), 2)
        self.env_values["mars_base_external_temperature"] = round(random.uniform(0, 21), 2)
        self.env_values["mars_base_internal_humidity"] = round(random.uniform(50, 60), 2)
        self.env_values["mars_base_external_illuminance"] = round(random.uniform(500, 715), 2)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 4)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    def get_env(self):
        '''
        DummySensor 클래스는 get_env() 메소드를 추가하는데 get_env() 메소드는 env_values를 return 한다.
        bonus: 출력하는 내용을 날짜와시간, 화성 기지 내부 온도, 화성 기지 외부 온도, 화성 기지 내부 습도 ,화성 기지 외부 광량, 
        화성 기지 내부 이산화탄소 농도, 화성 기지 내부 산소 농도 와 같이 파일에 log를 남기는 부분을 get_env()에 추가 한다.
        '''
        # 로그 파일에 기록

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

        return self.env_values

# 인스턴스 생성 및 테스트
if __name__ == "__main__":
    # DummySensor 클래스를 ds라는 이름으로 인스턴스(Instance)로 만든다.
    ds = DummySensor()
    # 인스턴스화 한 DummySensor 클래스에서 set_env()와 
    ds.set_env()
    # get_env()를 차례로 호출해서 값을 확인한다.
    env_data = ds.get_env()

    # 콘솔에도 출력
    for key, value in env_data.items():
        print(f"{key}: {value}")
