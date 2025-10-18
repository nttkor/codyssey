# 문제3. mission_computer_main.log를 읽어
# evaluation/mission_computer_main.log

#  출력은 총 4번 해야한다.
#  우선 f.read()로 읽은 데이트를 return 받는데 하나의 스트링이다.
#  이걸 split('\n') splitlines가 있는 모양
#  전체 출력
#  다음 split(',',2)로 얖에 time,event,log를 분리하는데 쉼표는 2개만 분리하고 로그 쉼표는 나둔다.
#  분리후 event field는 없애고고 time과 tuple만으로 tuple_list를 만들고 시간역순(내림차순)으로 정렬한후 객체 리스트를 전체 출력한다.
#  Dict으로 변환하여 출력 정렬리스트를 {timestamp:message} 그대로 출력 중첩없음 utf-8 json포맷

# 정렬기준 timestamp %Y-%m-%d:%M%S 빈줄은 무시 각행은 split(',',2)로 파싱

# 코드컨벤션 PEP8 준수


# 예외처리 
# 파일을 열수없는 경우
# 디코딩오류
# 로그포맷오류
# 처리단계오류
# 예외가 발생되면 print()로 해당메세지 출력하고 return으로 흐름 종료
# exit(), sys.exit()사용종료 안됨
# try-except사용가능하나 위와 동일한 문자가 나와야함.
#  예외처리 우선순위 - 
#  파일열기실패 - Fileopen Error.
#  디코딩오류 - Decoding Error.
#  로그포맷오류 - Invalid Log Format.
#  처리단계오류 - Processing Error.

import json
from datetime import datetime

LOG_PATH = 'evaluation/mission_computer_main.log'

def read_log_file(path):
    """
    로그 파일 읽기
    예외:
        파일열기실패 -> Fileopen Error.
        디코딩오류 -> Decoding Error.
    """
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, IOError):
        print('Fileopen Error.')
        return None
    except UnicodeDecodeError:
        print('Decoding Error.')
        return None

def parse_log_data(log_data):
    """
    로그 데이터를 파싱해서 (timestamp, message) 튜플 리스트로 변환
    예외:
        로그포맷오류 -> Invalid Log Format.
        처리단계오류 -> Processing Error.
    """
    try:
        if not log_data:
            raise RuntimeError  # 파일 읽기 실패 시 None 반환 고려

        lines = log_data.splitlines()
        if not lines or lines[0] != 'timestamp,event,message':
            raise ValueError  # 헤더 불일치

        log_list = []
        for line in lines[1:]:
            if not line.strip():
                continue  # 빈줄 무시
            parts = line.split(',', 2)  # 최대 2번만 분리
            if len(parts) != 3:
                raise ValueError
            timestamp, event, message = parts

            # timestamp 유효성 체크 (로그 형식에 맞춤)
            try:
                datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError

            log_list.append((timestamp, message))

        return log_list
    except ValueError:
        print('Invalid Log Format.')
        return None
    except Exception:
        print('Processing Error.')
        return None

def main():
    log_data = read_log_file(LOG_PATH)
    if log_data is None:
        return

    log_list = parse_log_data(log_data)
    if log_list is None:
        return

    # 출력1: 원본 문자열
    print(log_data)

    # 출력2: 파싱된 튜플 리스트
    print(log_list)

    # 출력3: timestamp 내림차순 정렬
    try:
        sorted_list = sorted(log_list, key=lambda x: x[0], reverse=True)
        print(sorted_list)
    except Exception:
        print('Processing Error.')
        return

    # 출력4: dict 변환 후 JSON 출력
    try:
        log_dict = dict(sorted_list)
        print(json.dumps(log_dict, ensure_ascii=False, indent=2))
    except Exception:
        print('Processing Error.')
        return

if __name__ == '__main__':
    main()
