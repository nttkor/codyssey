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
# exit(), sys.exit()사용종료
# try-except사용가능하나 위와 동일한 문자가 나와야함.
#  예외처리 우선순위 - 
#  파일열기실패 - Fileopen Error.
#  디코딩오류 - Decoding Error.
#  로그포맷오류 - Invalid Log Format.
#  처리단계오류 - Processing Error.

iimport json
from datetime import datetime


def read_file():
    """
    mission_computer_main.log 파일을 읽어 문자열로 반환.
    예외 발생 시 상위로 전달.
    """
    try:
        with open("evaluation/mission_computer_main.log", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        raise  # 모든 예외를 상위로 전달


def main():
    try:
        data = read_file()
        if not data:
            return  # 파일이 비어있으면 종료

        lines = data.splitlines()
        print("전체 출력:")
        print(data)

        log_entries = []

        for line in lines:
            if not line.strip():
                continue

            # timestamp, event, message 분리 (쉼표 2개만 분리)
            parts = line.split(",", 2)
            if len(parts) != 3:
                raise ValueError("Invalid Log Format.")

            timestamp_str, event, message = parts

            # timestamp 형식 확인
            try:
                datetime.strptime(timestamp_str, "%Y-%m-%d:%H%M%S")
            except ValueError:
                raise ValueError("Invalid Log Format.")

            # 데이터 검증 예시: 메시지가 비어있으면 오류
            if not message.strip():
                raise ValueError("Invalid Data: empty message")

            # event 필드는 사용하지 않고 timestamp와 message만 저장
            log_entries.append((timestamp_str, message))

        # 시간 역순 정렬
        log_entries.sort(
            key=lambda x: datetime.strptime(x[0], "%Y-%m-%d:%H%M%S"),
            reverse=True,
        )

        print("\n시간 역순 정렬된 로그:")
        for entry in log_entries:
            print(entry)

        # 딕셔너리 변환 및 JSON 출력
        log_dict = {timestamp: message for timestamp, message in log_entries}
        print("\nDict로 변환된 로그:")
        print(json.dumps(log_dict, ensure_ascii=False, indent=4))

    except (FileNotFoundError, IOError):
        print("Fileopen Error.")
        return
    except UnicodeDecodeError:
        print("Decoding Error.")
        return
    except ValueError as e:
        print(e)
        return
    except Exception:
        print("Processing Error.")
        return


if __name__ == "__main__":
    main()
