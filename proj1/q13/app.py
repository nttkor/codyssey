# socket 모듈을 import하여 현재 컴퓨터의 호스트 이름을 가져올 수 있게 함
# socket 모듈은 저수준 네트워크 인터페이스를 제공하여 네트워크 통신을 위한 소켓 프로그래밍을 가능하게 합니다. 
# TCP/IP, UDP 등 다양한 프로토콜을 지원하며, 클라이언트와 서버 간의 통신을 구축하는 데 사용됩니다.  
import socket

# Flask 프레임워크 import
# render_template은 flask에서 제공하는 함수로 지정한 폴더에 존재하는 html파일을 읽어오는 함수이다.
from flask import Flask, render_template

# Flask 앱 생성
app = Flask(__name__)

# 홈 페이지 라우팅
@app.route("/")
def home():
    # debug 모드가 활성화된 경우에만 호스트 이름을 표시하도록 설정
    if app.debug:
        # socket.gethostname() 함수는 현재 컴퓨터의 호스트 이름을 반환
        hostname = '컴퓨터(인스턴스) : ' + socket.gethostname()
    else:
        # debug 모드가 아닐 경우 빈 문자열 반환
        hostname = ' '

    # index.html 템플릿을 렌더링하면서, computername 변수에 hostname 값을 전달
    return render_template("index.html", computername=hostname)

# 앱 실행 (debug 모드를 True로 설정하여 개발 중 디버깅 가능하게 함)
if __name__ == "__main__":
    app.run(debug=True)
