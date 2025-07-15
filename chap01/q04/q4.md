# Git 사용법
1. Git 설치:
터미널에서 다음 명령어를 입력하여 Git을 설치합니다. 
- sudo apt update
- sudo apt install git

2. Git 초기 설정:
Git을 처음 사용하는 경우, 사용자 이름과 이메일 주소를 설정해야 합니다. 
- git config --global user.name "Your Name"
- git config --global user.email "your_email@example.com"

3. 저장소 초기화:
로컬 저장소를 만들거나 기존 저장소를 사용하려면 다음과 같이 합니다. 새 저장소 만들기. 
    - mkdir <저장소 이름>
    - cd <저장소 이름>
    - git init

4. 기존 저장소 복제. 
    - git clone <저장소 URL>

5. 파일 관리:
파일 추가. 

    - git add <파일명>  # 특정 파일 추가
    - git add .       # 모든 파일 추가
커밋. 
    - git commit -m "커밋 메시지"
원격 저장소에 업로드. 
코드

    - git push origin main  # main 브랜치에 업로드 (원격 저장소 이름은 origin)

6. 기타 유용한 명령어:
- git status: 현재 상태 확인
- git log: 커밋 기록 확인
- git diff: 변경 내용 확인
- git pull: 원격 저장소에서 변경 내용 가져오기
- git branch: 브랜치 관리
- git checkout: 브랜치 전환
- git merge: 브랜치 병합 
- 참고:
    Git 명령어에 대한 자세한 내용은 git --help 또는 온라인 문서에서 확인할 수 있습니다.
    GitHub와 같은 원격 저장소를 사용하면 여러 사람과 협업하여 프로젝트를 진행할 수 있습니다. 

1. 깃 설치

    1. 패키지 업데이트
        - sudo apt update

    2. 깃 설치
        - sudo apt install git

    3. 설치 확인
    git --version
    
    4. 깃 설정
        - git config --global user.name "jelog"
        - git config --global user.email "jelog@mail.com"
    

2. 깃 설정 확인
    0. 정보환인
        - git config -l
 
    1. 사용자 정보 확인
        - git config user.name
        - git config user.eamil
    
    2. 전역 설정 확인
        - git config --global --list

    3. 로컬 설정 확인
        - git config --local --list

    4. 리모트 저장소 확인
        - git remote -v


    5. 깃 구성 파일 확인
        - cat ~/.gitconfig
3. git 생성
4. git 클론
    - git clone https://github.com/tm-kr/portfolio.git

3. 깃 삭제

    1. 깃 패키지 제거
        - sudo apt remove git

    2. 설정 및 데이터 파일 제거
        - sudo rm -rf ~/.gitconfig

    3. 설치 확인
        - git --version