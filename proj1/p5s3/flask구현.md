Ubuntu VS Code로 다음과제를 처리하고 싶어 Flask로 만들까 문제 1. 음성 처리 수행 과제 시스템의 마이크를 인식하고 음성을 녹음하는 부분을 완성한다. 시스템의 마이크를 인식하고 음성을 녹음하는 부분은 외부 라이브러리를 사용하는 것이 가능하다. 파일들은 파이썬 앱이 실행되고 있는 하위에 records 폴더에 모두 저장된다. 파일의 이름은 녹음 날짜와 시간을 참조해서 ‘년월일-시간분초’와 같은 형태로 저장한다. 작성한 코드는 javis.py로 저장한다. 보너스 과제 특정 범위의 날짜의 녹음 파일을 보여주는 기능을 추가한다.
Flask로 음성 녹음 시스템을 구현하는 방법을 안내해 드리겠습니다. VS Code를 사용하면 개발 환경을 쉽게 설정할 수 있습니다. 이 프로젝트를 완성하기 위해 필요한 주요 기술 스택은 다음과 같습니다.
Flask: 웹 서버 역할을 수행하여 사용자와 상호작용하는 인터페이스를 제공합니다.
JavaScript (Web API): 브라우저의 마이크에 접근해 녹음 기능을 구현합니다. 파이썬만으로는 마이크 녹음이 불가능하며, 클라이언트(브라우저) 측에서 녹음해야 합니다.
Python (librosa): 녹음 파일을 서버에서 처리하는 데 사용됩니다.
프로젝트 구조
먼저, 프로젝트의 디렉터리 구조를 설정합니다.
javis_project/
├── records/ # 녹음 파일 저장 폴더
├── static/ # 정적 파일(스크립트, CSS)
│   └── js/
│       └── recorder.js
├── templates/ # HTML 템플릿 파일
│   └── index.html
└── javis.py # 메인 Flask 애플리케이션 파일
1. Flask 애플리케이션 (javis.py)
Flask 서버를 설정하고, records 폴더를 생성하며, 파일을 업로드할 경로를 정의합니다.
python
import os
import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# records 폴더 생성 (없으면)
RECORDS_FOLDER = 'records'
if not os.path.exists(RECORDS_FOLDER):
    os.makedirs(RECORDS_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400

    audio_file = request.files['audio']
    
    # 파일 이름 형식: '년월일-시간분초.wav'
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f'{timestamp}.wav'
    filepath = os.path.join(RECORDS_FOLDER, filename)

    audio_file.save(filepath)
    return jsonify({'message': 'Audio recorded and saved successfully', 'filename': filename}), 200

@app.route('/get_recordings', methods=['GET'])
def get_recordings():
    files = sorted([f for f in os.listdir(RECORDS_FOLDER) if f.endswith('.wav')], reverse=True)
    return jsonify(files)

# 보너스 과제: 특정 날짜 범위의 파일 가져오기
@app.route('/get_recordings_by_date', methods=['GET'])
def get_recordings_by_date():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')

    files = os.listdir(RECORDS_FOLDER)
    filtered_files = []
    for filename in files:
        if filename.endswith('.wav'):
            try:
                file_date_str = filename.split('-')[0]
                file_date = datetime.datetime.strptime(file_date_str, '%Y%m%d')
                if start_date <= file_date <= end_date:
                    filtered_files.append(filename)
            except (ValueError, IndexError):
                continue

    filtered_files.sort(reverse=True)
    return jsonify(filtered_files)

@app.route('/records/<filename>')
def serve_audio(filename):
    return send_from_directory(RECORDS_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
코드를 사용할 때는 주의가 필요합니다.

2. 웹 페이지 (templates/index.html)
사용자 인터페이스를 정의합니다. 마이크 접근 권한 요청, 녹음 시작/중지 버튼, 녹음 파일 목록 표시 기능을 포함합니다.
html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Javis 음성 녹음</title>
</head>
<body>
    <h1>음성 녹음 시스템</h1>
    <div>
        <button id="startRecording">녹음 시작</button>
        <button id="stopRecording" disabled>녹음 중지</button>
    </div>
    <div id="status">대기 중...</div>

    <hr>

    <h2>녹음 파일 목록</h2>
    <div id="recordingList"></div>

    <hr>
    
    <h2>보너스 과제: 날짜별 검색</h2>
    <form id="dateRangeForm">
        <label for="startDate">시작 날짜:</label>
        <input type="date" id="startDate">
        <label for="endDate">종료 날짜:</label>
        <input type="date" id="endDate">
        <button type="submit">검색</button>
    </form>
    <div id="filteredRecordingList"></div>

    <script src="{{ url_for('static', filename='js/recorder.js') }}"></script>
</body>
</html>
코드를 사용할 때는 주의가 필요합니다.

3. 클라이언트 측 스크립트 (static/js/recorder.js)
사용자 브라우저에서 마이크 녹음을 제어하고, 녹음된 오디오를 Flask 서버로 보냅니다.
javascript
document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('startRecording');
    const stopButton = document.getElementById('stopRecording');
    const statusDiv = document.getElementById('status');
    const recordingListDiv = document.getElementById('recordingList');
    const filteredRecordingListDiv = document.getElementById('filteredRecordingList');
    const dateRangeForm = document.getElementById('dateRangeForm');

    let mediaRecorder;
    let audioChunks = [];

    // 녹음 시작
    startButton.addEventListener('click', async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            
            startButton.disabled = true;
            stopButton.disabled = false;
            statusDiv.textContent = '녹음 중...';

            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

        } catch (err) {
            statusDiv.textContent = '마이크 접근에 실패했습니다: ' + err;
            console.error('Error accessing microphone:', err);
        }
    });

    // 녹음 중지
    stopButton.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            mediaRecorder.addEventListener('stop', () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                sendAudioToServer(audioBlob);
                audioChunks = [];
            });
            startButton.disabled = false;
            stopButton.disabled = true;
            statusDiv.textContent = '녹음이 완료되었습니다. 서버에 업로드 중...';
        }
    });

    // 서버로 오디오 파일 전송
    async function sendAudioToServer(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');

        try {
            const response = await fetch('/upload_audio', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            statusDiv.textContent = result.message;
            loadRecordingList(); // 녹음 완료 후 목록 새로고침
        } catch (err) {
            statusDiv.textContent = '서버 업로드 실패: ' + err;
            console.error('Error uploading audio:', err);
        }
    }

    // 녹음 파일 목록 불러오기
    async function loadRecordingList() {
        try {
            const response = await fetch('/get_recordings');
            const files = await response.json();
            displayRecordings(files, recordingListDiv);
        } catch (err) {
            recordingListDiv.innerHTML = '<li>파일 목록을 불러오는 중 오류가 발생했습니다.</li>';
        }
    }

    // 녹음 파일 목록 화면에 표시
    function displayRecordings(files, container) {
        container.innerHTML = '';
        if (files.length === 0) {
            container.innerHTML = '<li>녹음된 파일이 없습니다.</li>';
        } else {
            const ul = document.createElement('ul');
            files.forEach(filename => {
                const li = document.createElement('li');
                const link = document.createElement('a');
                link.href = `/records/${filename}`;
                link.textContent = filename;
                link.target = "_blank"; // 새 탭에서 열기
                li.appendChild(link);
                ul.appendChild(li);
            });
            container.appendChild(ul);
        }
    }

    // 날짜 범위 검색
    dateRangeForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;

        if (!startDate || !endDate) {
            alert('날짜 범위를 선택하세요.');
            return;
        }

        try {
            const response = await fetch(`/get_recordings_by_date?start_date=${startDate}&end_date=${endDate}`);
            const files = await response.json();
            displayRecordings(files, filteredRecordingListDiv);
        } catch (err) {
            filteredRecordingListDiv.innerHTML = '<li>날짜 검색 중 오류가 발생했습니다.</li>';
        }
    });

    // 페이지 로딩 시 목록을 즉시 불러옴
    loadRecordingList();
});
코드를 사용할 때는 주의가 필요합니다.

4. 실행 방법
VS Code에서 터미널 열기: Ctrl + Backtick()을 눌러 터미널을 엽니다.
가상 환경 생성 및 활성화:
bash
python3 -m venv venv
source venv/bin/activate
코드를 사용할 때는 주의가 필요합니다.

필요 라이브러리 설치:
bash
pip install Flask
코드를 사용할 때는 주의가 필요합니다.

Flask 애플리케이션 실행:
bash
flask run
코드를 사용할 때는 주의가 필요합니다.

브라우저에서 접속: 터미널에 표시되는 URL(http://127.0.0.1:5000/)로 접속합니다.
마이크 권한 허용: 브라우저에서 마이크 접근 권한을 요청하면 허용합니다.
녹음 시작/중지: 버튼을 눌러 음성을 녹음하고 저장된 파일을 확인합니다.
AI 대답에는 오류가 있을 수 있습니다. 자세히 알아보기