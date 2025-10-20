문제3. mission-computer_main.log를 읽어


 출력은 총 4번 해야한다.
 우선 f.read()로 읽은 데이트를 return 받는데 하나의 스트링이다.
 이걸 split('\n') splitlines()로 라인 분리된 리스트 만들어)
        log_list = []
        log_lines = log_list.splitlines()
        #첫번째 줄이 헤더인데 헤더 체크
        if log_lines[0] != 'timestamp,event,message':
            raise ValueError
        # 다음 tuple을 만들어 sort()해야 하는데 헤더 빼고 처리 list 1부터 시작
        for logs in log_lines[1:]:
 전체 출력
 
 다음 split(',',2)로 얖에 time,event,log를 분리하는데 쉼표는 2개만 분리하고 3번째 로그안에 포함된 쉼표는 나둔다. 분리후 3개가 안되는건 에러처리 raise ValidError
 분리후 event field는 없애고고 time과 tuple만으로 tuple_list를 만들고 시간역순(내림차순)으로 정렬한후 객체 리스트를 전체 출력한다.
 Dict으로 변환하여 출력 정렬리스트를 {timestamp:message} 그대로 출력 중첩없음 utf-8 json포맷

정렬기준 timestamp %Y-%m-%d:%M%S 빈줄은 무시 각행은 split(',',2)로 파싱

코드컨벤션 PEP8 준수


예외처리 
파일을 열수없는 경우
디코딩오류
로그포맷오류
처리단계오류
예외가 발생되면 print()로 해당메세지 출력하고 return으로 흐름 종료
exit(), sys.exit()사용종료 안됨
try-except사용가능하나 위와 동일한 문자가 나와야함.
 예외처리 우선순위 - 
 파일열기실패 - Fileopen Error.
 디코딩오류 - Decoding Error.
 로그포맷오류 - Invalid Log Format.
 처리단계오류 - Processing Error.

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