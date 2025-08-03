# 문제3 소스코드 관리는 꼭 필요한 것만

[상위폴더](../../proj1/)

__pycache__와 .venv 가 뭐지  

편집  
__pycache__와 .venv는 Python 개발 과정에서 자동으로 생성되는 디렉토리들입니다. 각각의 역할을 설명드리겠습니다.  

__pycache__ 디렉토리  
역할  
Python이 .py 파일을 실행할 때 자동으로 생성되는 바이트코드 캐시 폴더
Python 코드를 더 빠르게 실행하기 위해 컴파일된 바이트코드(.pyc 파일)를 저장  
생성 과정  
python  
* app.py 파일이 있을 때  
print("Hello World")  
파일을 실행하면:  

project/  
├── app.py  
└── __pycache__/  
    └── app.cpython-39.pyc  # 컴파일된 바이트코드  
왜 Git에서 제외해야 하는가?  
자동 생성: 코드 실행 시마다 자동으로 만들어짐  
환경 의존적: Python 버전에 따라 다름  
불필요: 소스코드만 있으면 언제든 재생성 가능  
용량 증가: 저장소 크기만 늘림  
.venv 디렉토리  
역할  
Python 가상환경(Virtual Environment) 폴더  
프로젝트별로 독립적인 Python 패키지 환경을 제공  
생성 방법
bash
* 가상환경 생성
python -m venv .venv

* 가상환경 활성화
source .venv/bin/activate  # Linux/Mac  
.venv\Scripts\activate     # Windows  
디렉토리 구조  
.venv/  
├── bin/          # 실행 파일들 (Linux/Mac)  
├── Scripts/      # 실행 파일들 (Windows)   
├── lib/          # 설치된 패키지들  
├── include/      # 헤더 파일들  
└── pyvenv.cfg    # 가상환경 설정  
왜 Git에서 제외해야 하는가?
용량이 큼: 설치된 모든 패키지가 포함되어 수백 MB  
환경 의존적: OS나 Python 버전에 따라 다름  
재생성 가능: requirements.txt로 언제든 재생성 가능  
개인적: 각 개발자가 자신의 환경에서 생성해야 함  
올바른 Python 프로젝트 구조  
Git에 포함해야 할 것:  
project/
├── app.py                 # ✅ 소스코드  
├── requirements.txt       # ✅ 패키지 목록  
├── .gitignore            # ✅ Git 제외 파일 목록  
└── README.md             # ✅ 프로젝트 설명  
Git에서 제외해야 할 것:
project/  
├── __pycache__/          # ❌ 바이트코드 캐시  
├── .venv/                # ❌ 가상환경  
├── *.pyc                 # ❌ 개별 바이트코드 파일  
└── .env                  # ❌ 환경변수 파일 (민감한 정보)  
requirements.txt 활용
가상환경 대신 패키지 목록을 공유:

bash
* 현재 환경의 패키지 목록 저장
pip freeze > requirements.txt

* 다른 환경에서 패키지 설치
pip install -r requirements.txt
이렇게 하면 .venv 폴더 없이도 누구나 동일한 개발 환경을 구성할 수 있습니다.

따라서 .gitignore에 이 두 디렉토리를 추가하는 것은 Python 프로젝트의 표준 관례이며, 저장소를 깔끔하게 유지하고 협업을 원활하게 만드는 중요한 작업입니다.