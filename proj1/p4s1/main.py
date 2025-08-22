import json
import os

# 로그 파일 읽기
def search_logs(log_dict, search_term):
    """로그 딕셔너리에서 검색어를 포함한 로그를 찾아 출력"""
    search_term = search_term.lower()
    found_logs = []
    for timestamp, item in log_dict.items():
        if timestamp == "header":  # header는 건너뛰기
            continue
        event,message = item
        if search_term in message.lower():
            found_logs.append((timestamp, event, message))
    return found_logs

def main():
    log = str()
    log_list = list()
    os.chdir('/home/mpeg4/Codyssey/proj1/p4s1')

    # 예외를 한 번에 처리할 try-except 구문
    try:
        with open('mission_computer_main.log', 'r', encoding='utf-8') as file:
            log = file.read()
        # 로그 출력
        print(f"\nmission_computer_main.log 파일을 읽어 전체 내용{type(log)}을 화면에 출력:")
        print('=' * 100)  
        print(log)
        
        # 로그 파일 내용을 콤마(,)를 기준으로 날짜/시간과 메시지를 분리하여 Python의 리스트(List) 객체로 전환
        for line in log.splitlines():
            if not line.strip():  # 빈 줄은 건너뜀
                continue
            try:
                timestamp, event, message = line.strip().split(',', 2)
                log_list.append([timestamp, event, message])
            except ValueError:
                print(f"로그 형식 오류: '{line.strip()}' 줄을 건너뜁니다.")
                continue
    except (FileNotFoundError, UnicodeDecodeError, IOError, ValueError) as e:
        # 모든 예외를 한번에 처리
        print(f"예외 발생: {str(e)}")
        raise  # 예외를 다시 발생시켜 호출한 곳에서 처리하게끔 함
    # 리스트객체를 화면에출력
    print(f"\n리스트 객체{type(log_list)}를 화면에 출력:")
    print('=' * 100)
    print(*log_list,sep='\n')
    # 시간 역순으로 정렬 (datetime 모듈 없이 문자열 비교)
    log_list.sort(key=lambda x: x[0], reverse=True)

    # 역순으로 정렬된 리스트객채 출력
    print(f"\n시간 역순으로 정렬된 리스트개개체{type(log_list)}로그:")
    print('=' * 100)  
    # for log in log_list:
    #     print(log)
    print(*log_list, sep='\n')

    # 사전 형태로 변환
    log_dict = {log[0]: [log[1], log[2]] for log in log_list[1:]}
    # dict의 첫 번째 항목을 header로 추가
    log_dict = {"header": log_list[0]} | log_dict
    # JSON 파일로 저장
    try:
        with open('mission_computer_main.json', 'w', encoding='utf-8') as json_file:
            json.dump(log_dict, json_file, ensure_ascii=False, indent=4)
        print("\n로그가 mission_computer_main.json 파일로 저장되었습니다.")
    except IOError as e:
        print(f"파일 저장 중 오류가 발생했습니다: {str(e)}")
        raise

    # 위험 단어 리스트
    danger_keywords = [
        "unstable", "explosion", "Oxygen", "Damage", "falut", 
        "Leak", "Pressure", "Overheating", "Bad", "failure", 
        "Collision", "Emergency"
    ]

    # 사고원인 분석 보고서 생성
    try:
        with open("log_analysis.md", 'w', encoding='utf-8') as report_file:
            # 마크다운 테이블 헤더 작성
            report_file.write("# 사고원인 분석보고서\n\n")
            report_file.write("이 보고서는 위험 단어가 포함된 로그 메시지를 기반으로 작성되었습니다.\n\n")
            report_file.write("| timestamp           | event | message                                   |\n")
            report_file.write("|---------------------|-------|-------------------------------------------|\n")
            
            # 위험 단어가 포함된 로그 메시지 추가
            for log_entry in log_list:
                timestamp, event, message = log_entry
                # 위험 단어가 메시지에 포함되어 있으면 해당 메시지를 테이블에 추가
                if any(keyword in message for keyword in danger_keywords):
                    # 마크다운 테이블 형식으로 각 로그 항목을 작성
                    report_file.write(f"| {timestamp} | {event} | {message} |\n")

            print("\n사고원인 분석보고서(log_analysis.md)가 생성되었습니다.")
    except IOError as e:
        print(f"보고서 파일 저장 중 오류가 발생했습니다: {str(e)}")
        raise  # 오류를 호출한 곳에서 처리하도록 예외를 다시 발생시킴

    # 위험 단어가 포함된 로그만 별도로 warning.log로 저장
    try:
        with open('warning.log', 'w', encoding='utf-8') as warning_file:
            for log_entry in log_list:
                timestamp, event, message = log_entry
                if any(keyword in message for keyword in danger_keywords):
                    warning_file.write(f"{timestamp},{event},{message}\n")
            print("\n위험 단어가 포함된 로그(warning.log)가 생성되었습니다.")
    except IOError as e:
        print(f"위험 로그 파일 저장 중 오류가 발생했습니다: {str(e)}")
        raise  # 오류를 호출한 곳에서 처리하도록 예외를 다시 발생시킴

    with open('mission_computer_main.log', 'r', encoding='utf-8') as log_file:
        logs = log_file.readlines()
    print(f"\n로그를 시간의 역순으로 정렬하여 출력: type(logs)={type(logs)}")
    print('=' * 100)
    print(*logs[::-1])  # 역순으로 출력

    # 사용자 입력 필터링 기능
    while True:

        # 추천 단어 리스트 출력
        print("\n단어검색기능 - 검색종료 0")
        for i, keyword in enumerate(danger_keywords[:9], start=1):
            print(f"{i}: {keyword}", end=" ")

        user_input = input("\n1~9 사이의 숫자를 입력하면 해당 단어로 검색합니다 (0 입력 시 검색 종료): ").strip()

        if user_input == '0':
            break

        if len(user_input) ==1 and user_input in '123456789':
            # 숫자가 1~10 사이인지 체크하고 해당 단어로 검색
            selected_index = int(user_input) - 1
            search_term = danger_keywords[selected_index]
        else:
            search_term = user_input

        print(f"검색어 '{search_term}'로 검색 중...")
        # 검색된 로그 출력
        found_logs = search_logs(log_dict, search_term)
        if found_logs:
            print(f"\n검색어 '{search_term}'와 일치하는 로그 {len(found_logs)}건 발견했습니다.")
            for log in found_logs:
                print(f"\t{log[0]} | {log[1]} | {log[2]}")
            print()
        else:
            print(f"\n검색어 '{search_term}'와 일치하는 로그가 없습니다.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"프로그램 실행 중 오류가 발생했습니다: {str(e)}")
