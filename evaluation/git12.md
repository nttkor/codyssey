## 1.새브런치를 만들고 즉시 그 브랜치로 전환
- git checkout -b new 
## 2. 가장 최근 커밋의 커밋메세지만 수정하는 명령어
- git commit --amend
## 3. 병합도중 충돌이 발생 병함이 중단된 상황에서 이를 되돌리는 명령어
- git merge --abort
4,5,6, 한묶음 function이름도 q4, q5, q6으로 해야함
## 4. 원격저장소의 최신 커밋 정보를 가져오기만하고 자동병합하지 않는 명령어
- git fetch
## 5. 현재 브랜치를 원격브랜치 origin/new_feature와 upstream 추적만 설정하는 명령어
- git branch -u origin/new-feature
# 6. 최근 커밋은 취소하돼 변경내용은 스테이징 상태유지
- git reset --soft HEAD^
 
 문제3. mission-computer_main.log를 읽어


 출력은 총 4번 해야한다.
 우선 f.read()로 읽은 데이트를 return 받는데 하나의 스트링이다.
 이걸 split('\n') splitlines가 있는 모양
 전체 출력
 다음 split(',',2)로 얖에 time,event,log를 분리하는데 쉼표는 2개만 분리하고 로그 쉼표는 나둔다.
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
exit(), sys.exit()사용종료
try-except사용가능하나 위와 동일한 문자가 나와야함.
 예외처리 우선순위 - 
 파일열기실패 - Fileopen Error.
 디코딩오류 - Decoding Error.
 로그포맷오류 - Invalid Log Format.
 처리단계오류 - Processing Error.