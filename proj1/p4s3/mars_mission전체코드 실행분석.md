# mars\_mission\_computer 실행 해설 (상세 Markdown)

## 1) 한 번에 보는 전체 흐름 (요약 시나리오)

1. **메인 시작** (`if __name__ == '__main__'`)

   * 현재 파일 경로로 작업 디렉터리 고정 → `sensor_log.txt`/`setting.txt`가 같은 폴더에 위치하도록.
   * **멀티프로세싱용 Event**(`stop_event`) 생성. (즉시 종료 신호에 사용)
   * 안내 메시지: "멀티프로세스 및 멀티스레드 실행 시작" 출력.
2. **멀티프로세스 시작** (`run_processes`)

   * **서로 다른 목표 함수**를 수행하는 **3개 프로세스**를 시작:

     * `Process-MC1`: `get_sensor_data()`
     * `Process-MC2`: `get_mission_computer_info()`
     * `Process-MC3`: `get_mission_computer_load()`
   * 각 프로세스는 **독립적인 `MissionComputer` 인스턴스**를 가짐.
3. **멀티스레드 시작** (`run_threads`를 별도 스레드로 실행)

   * `Thread-MC`라는 **하나의 `MissionComputer` 인스턴스**에서 **3개 스레드**를 생성:

     * 스레드1: `get_sensor_data()`
     * 스레드2: `get_mission_computer_info()`
     * 스레드3: `get_mission_computer_load()`
4. **사용자 입력 대기** (`wait_for_exit`)

   * 콘솔에서 `q` 입력 시 `stop_event.set()` 호출 → **모든 루프가 즉시 종료 경로**로 진입.
   * `Ctrl+C`(KeyboardInterrupt)도 동일하게 종료 신호 설정.
5. **정리 단계**

   * **프로세스**는 `terminate()` 후 `join()` (즉시 종료 보장).
   * **스레드**는 `stop_event`를 감지하여 자연 종료 → `join()`로 합류.
   * 종료 메시지: "모든 스레드 및 프로세스 종료 완료"

---

## 2) 각 컴포넌트 설명

### A. DummySensor (문제 1 + 보너스)

* `env_values`: 다음 키를 보유하는 환경 딕셔너리

  * 내부/외부 온도, 내부 습도, 외부 광량, 내부 CO2, 내부 산소
* `set_env()`: **지정된 범위**(과제 명세)에 따라 난수 생성 → `env_values` 갱신
* `get_env()`: 현재 값을 **복사 반환**하며, 동시에 **`sensor_log.txt`에 로그**를 남김 (보너스 충족)

  * 포맷: `YYYY-MM-DD HH:MM:SS, 값1, 값2, ...`

### B. MissionComputer (문제 2, 3, 4 + 보너스)

* **속성**

  * `ds`: DummySensor 인스턴스
  * `env_values`: 최근 센서 값 저장
  * `stop_event`: 즉시 종료를 위한 이벤트
  * `sensor_history`: 5분 평균 계산용 저장소 (길이 60이면 평균 계산)
  * `setting`: `setting.txt`로 **출력 항목을 제어** (문제 3 보너스)
* **메서드**

  * `load_setting()`: `setting.txt` 값(`key=true/false`)을 읽어 **출력 항목 스위치** 결정
  * `get_sensor_data()` (문제 2)

    * 5초마다: `ds.set_env()` → `ds.get_env()` → `env_values` 저장/출력(JSON)
    * 60회(=5분)마다: `print_5min_average()` 호출 후 히스토리 초기화 (보너스 충족)
  * `print_5min_average()`

    * `sensor_history`의 모든 항목에 대해 **키별 평균** 계산 후 JSON 출력
  * `get_mission_computer_info()` (문제 3)

    * 20초마다: OS/버전/CPU 타입/물리 코어/전체 메모리(MB)를 **선택적으로** JSON 출력
  * `get_mission_computer_load()` (문제 3)

    * 20초마다: CPU 사용률(1초 샘플링) 및 메모리 사용률을 **선택적으로** JSON 출력

---

## 3) 타이밍 & 루프 설계 (중요)

### 3-1. `responsive_sleep(duration, stop_event, interval=0.5)`

* **즉시 종료**(보너스) 달성을 위한 핵심 도우미.
* 일반 `time.sleep(5)`는 5초 동안 막히지만, 본 함수는 **0.5초 간격**으로 나누어 `stop_event`를 반복 체크 → **중간에도 깨어나 즉시 종료**.
* 모든 주기적 작업(`5초/20초`)에서 이 함수를 사용하여 **반응형 대기** 구현.

### 3-2. 주기 요약

* 센서 수집: **5초마다** (`get_sensor_data`) → 60회마다 **5분 평균** 출력
* 시스템 정보: **20초마다** (`get_mission_computer_info`)
* 시스템 부하: **20초마다** (`get_mission_computer_load`)

> 참고: `psutil.cpu_percent(interval=1)`은 **1초 블로킹**이므로, 그 1초 동안은 즉시 반응이 어렵지만, 나머지 대기는 `responsive_sleep(20)`으로 즉시 반응.

---

## 4) 멀티스레드 vs 멀티프로세스 구조 (핵심 비교)

### 4-1. 멀티스레드 (`run_threads`)

* 하나의 `MissionComputer(Thread-MC)` 인스턴스에서 **3개 스레드**가 동시에 동작:

  1. 센서 수집, 2) 시스템 정보, 3) 시스템 부하
* **메모리 공유**: 같은 인스턴스이므로 속성 접근/출력이 **공유**됨.
* **장점**: 컨텍스트 스위칭이 가볍고 공유 상태 접근이 빠름.
* **주의**: 콘솔 출력이 \*\*교차(interleaving)\*\*될 수 있음 (여러 스레드의 `print`가 뒤섞임).

### 4-2. 멀티프로세스 (`run_processes`)

* **서로 다른 프로세스**가 각기 별도의 `MissionComputer` 인스턴스를 생성:

  * `Process-MC1`: 센서 수집
  * `Process-MC2`: 시스템 정보
  * `Process-MC3`: 시스템 부하
* **프로세스 간 메모리 분리**: 상태가 독립적이며, 안정성(격리)이 높음.
* **이벤트 전달**: `multiprocessing.Event` 객체를 **자식 프로세스에 전달**하여 종료 신호를 공유.

  * 파이썬의 `multiprocessing.Event`는 **프로세스 간 동기화**가 가능하도록 설계되어, 자식에 전달 시 **종료 신호를 함께 공유**할 수 있음.
* **주의**: 서로 다른 프로세스의 콘솔 출력도 **교차**될 수 있으며, 운영체제에 따라 출력 타이밍이 다르게 보일 수 있음.

---

## 5) 즉시 종료(보너스) 메커니즘 상세

### 5-1. 입력 루프 (`wait_for_exit`)

* 콘솔에서 입력을 받고, \*\*소문자 'q'\*\*를 입력하면 `stop_event.set()` 실행 → 종료 신호 브로드캐스트.
* `Ctrl+C` 발생 시도 동일 처리.

### 5-2. 각 작업 루프에서의 반응 방식

* 모든 반복 루프의 **종료 조건**: `while not self.stop_event.is_set()`
* 대기 구간은 \*\*`responsive_sleep`\*\*로 쪼개져 있어, **최대 0.5초** 내로 종료 신호에 반응.
* `psutil.cpu_percent(interval=1)`의 **1초 대기**만은 즉시 끊기 어렵지만, 다음 사이클 대기에서는 곧바로 멈춤.

### 5-3. 프로세스 강제 종료 보강

* `q`를 눌러 이벤트가 세트되면, **스레드/프로세스는 자연 종료 경로**로 진입.
* 이후 메인에서 \*\*`p.terminate()`\*\*를 호출하여 **즉시 종료를 보장** (특히 긴 I/O 등으로 자연 종료가 지연될 때 대비).
* 그리고 `p.join()`으로 자원 회수.

> 결론: 이벤트+반응형 슬립으로 **즉시성**을 확보하고, 마지막에 `terminate()`로 **확실히 마무리**하는 이중 안전장치.

---

## 6) 5분 평균 계산 로직 (보너스)

* `get_sensor_data()`가 5초마다 한 번씩 `env_values`를 `sensor_history`에 추가.
* `len(sensor_history) >= 60`이면 (5초 × 60 = **300초 = 5분**) 평균 계산 시작.
* `print_5min_average()`

  * `sensor_history[0].keys()` 기준으로 각 키의 총합/개수 계산.
  * 소숫점 자리 반올림(`round`) 후 JSON으로 출력.
  * 출력 후 `sensor_history.clear()`로 다음 5분을 위한 초기화.

---

## 7) 파일 입출력과 설정

### 7-1. `sensor_log.txt`

* `DummySensor.get_env()` 호출 시 **한 줄씩 append**
* 포맷: `YYYY-MM-DD HH:MM:SS, v1, v2, v3, ...` (키는 포함하지 않음)
* 다량의 기록이 쌓이므로 로그 회전/보관 정책이 필요하다면 별도 관리 필요.

### 7-2. `setting.txt` (문제 3 보너스)

* 예시:

  ```
  os=true
  os_version=true
  cpu_type=false
  cpu_cores=true
  memory_total_MB=true
  cpu_usage_percent=true
  memory_usage_percent=true
  ```
* 잘못된 키는 무시되고, 파일이 없으면 **경고 출력** 후 **기본값(True)** 사용.

---

## 8) 실행 시 콘솔 출력 패턴 예시

```
== 멀티프로세스 및 멀티스레드 실행 시작 ==
[Process-MC1 - Sensor Data]
{ ... 센서 값 JSON ... }
[Thread-MC - System Info]
{ ... 시스템 정보 JSON ... }
[Thread-MC - System Load]
{ ... 부하 JSON ... }
...
[Thread-MC - 5분 평균]
{ ... 평균 JSON ... }
...
종료하려면 q를 입력하세요: q
== 모든 스레드 및 프로세스 종료 완료 ==
```

> **주의**: 스레드/프로세스가 동시에 `print`하므로, 서로 다른 블록이 섞여 보일 수 있습니다. (기능상 문제는 아님)

---

## 9) 안전성과 이식성 관련 메모

* **이벤트 전달**: `multiprocessing.Event`는 자식 프로세스에 전달되어 **동일한 종료 신호**를 공유.
* **플랫폼 차이**:

  * Windows는 프로세스 시작 방식이 `spawn`이므로, 본 코드처럼 `if __name__ == '__main__'` 가드는 **필수**이며 이미 적용됨.
  * `terminate()`의 동작은 OS에 따라 다를 수 있으나, 공통적으로 **즉시 종료** 성향을 가짐.
* **표준 출력 동기화**: 로그가 섞이는 것을 피하려면, 파일 로그를 프로세스/스레드별로 분리하거나, 큐/로거 핸들러를 통해 직렬화할 수 있음(참고 제안, 본 과제 범위 밖).

---

## 10) 과제 요구 사항 체크리스트

* **문제 1**: DummySensor 클래스 / 난수 범위 / `set_env()` / `get_env()` / 로그 기록(보너스) ✅
* **문제 2**: MissionComputer 클래스 / `env_values` / DummySensor 인스턴스 / `get_sensor_data()` 5초 주기 JSON 출력 / `RunComputer`(실제 인스턴스들) ✅
* **문제 2 보너스**: 키 입력 시 종료 / 5분 평균 출력 ✅
* **문제 3**: `get_mission_computer_info()`(OS/버전/CPU/코어/메모리) / `get_mission_computer_load()`(CPU/메모리 사용률) / JSON 출력 ✅
* **문제 3 보너스**: `setting.txt`로 출력 항목 제어 ✅
* **문제 4**: 20초 주기 결과 출력(정보/부하) / 3개 스레드 병행 실행 / 3개 프로세스 병행 실행 ✅
* **문제 4 보너스**: 실행 중 `q`로 **즉시 종료** (Event + responsive\_sleep + terminate 보강) ✅

---

## 11) 확장/개선 아이디어 (선택)

* **Graceful Shutdown 우선**: `q` 입력 시 `stop_event.set()`만으로도 대부분 즉시 종료됨 → `terminate()`는 최후 수단으로 유지(현재 코드는 안전을 위해 즉시 호출).
* **출력 정돈**: 프로세스/스레드별 **프리픽스** 또는 **구분 라인** 강화, 혹은 Python `logging` 모듈로 파일 분리.
* **로그 스키마 개선**: `sensor_log.txt`에 **키=값** 형태로 기록하거나, CSV 헤더를 포함해 가독성 향상.
* **CPU 측정 반응성 개선**: `psutil.cpu_percent(interval=None)` + 내부 타이머로 1초 블로킹 회피(과제 요구는 충족 중).

---

## 12) 빠른 디버깅 체크리스트

* `psutil` 미설치 시: `pip install psutil`
* `setting.txt` 누락 시: 경고 메시지 후 기본값 사용(정상 동작)
* 로그 파일 위치: 스크립트 파일과 **같은 폴더**(메인에서 `os.chdir(...)` 수행)
* 종료가 느리다?: `psutil.cpu_percent(interval=1)`의 1초 대기 때문일 수 있음 (다음 사이클에서 바로 멈춤)

---

**끝.** 이 문서는 코드 변경 없이 실행 시 실제 동작을 바탕으로 멀티스레드/멀티프로세스, 이벤트 기반 즉시종료, 주기 설계(5초/20초), 5분 평균 및 설정 파일 처리 흐름을 체계적으로 설명합니다.
