from flask import Flask, request, Response #웹 서버 만들기/클라이언트 요청 처리/응답 생성에 사용됩니다. 
import os
from io import BytesIO
from gtts import gTTS

DEFAULT_LANG = os.getenv('DEFAULT_LANG', 'ko') #환경 변수 DEFAULT_LANG를 읽고, 없으면 'ko'를 기본으로 설정합니다. 이를 통해 기본 언어를 쉽게 바꿀 수 있습니다.
app = Flask(__name__) #__name__을 인자로 해서 Flask 앱을 생성합니다. 이 앱은 라우트, 설정 등을 관리합니다.  

@app.route("/") #"/": 루트 경로에 들어오는 요청을 처리합니다.
def home():

    text = "Hello, DevOps"

    lang = request.args.get('lang', DEFAULT_LANG)   #lang: URL 쿼리 파라미터 ?lang=xx로 언어를 지정받거나, 지정이 없으면 DEFAULT_LANG를 사용합니다.
    fp = BytesIO() # 메모리 기반의 가상 파일 객체를 생성하는 코드입니다. 일반 파일처럼 읽기/쓰기, 포인터 이동 등의 기능을 제공하지만, 실제로 하드디스크에 파일을 만들지 않고 RAM에만 데이터를 저장합니다.
    gTTS(text, "com", lang).write_to_fp(fp)

    return Response(fp.getvalue(), mimetype='audio/mpeg') # 페이지 전달없이 바로 재생

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
    #