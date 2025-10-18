# javis
## 함수 호출 트리
mermaid
graph TD
    main --> record_audio
    main --> save_recording
    main --> process_recording
    main --> search_keyword

    process_recording --> save_transcription_as_csv
코드를 사용할 때는 주의가 필요합니다.

## 상세 설명
* main(): 프로그램의 진입점으로, while 반복문을 통해 전체 기능을 반복 실행합니다.
* record_audio(): 시스템 마이크에서 음성을 녹음하는 함수를 호출합니다.
* save_recording(): 녹음된 오디오 데이터를 WAV 파일로 저장하고, 파일 경로를 반환합니다.
* process_recording(): 저장된 WAV 파일 경로를 인자로 받아 STT 처리를 시작합니다.
* search_keyword(): 모든 기록이 저장된 CSV 파일을 읽어와 키워드를 검색합니다.
* process_recording():
* save_transcription_as_csv(): 인식된 텍스트를 인자로 받아 all_records.csv 파일에 추가하는 함수를 호출합니다.

## 데이터 흐름
* main() → record_audio(): duration, fs (초, 샘플링 주파수)
* record_audio() → main(): recording 데이터 (float64 numpy 배열)
* main() → save_recording(): recording 데이터, fs
* save_recording() → main(): filename (저장된 파일 경로)
* main() → process_recording(): filename
* process_recording() → save_transcription_as_csv(): text (STT 변환 결과)
* main() → search_keyword(): 호출 시 인자는 없으나, 내부적으로 사용자 입력을 받음
* 이 함수 트리는 javis.py가 어떻게 동작하는지 한눈에 보여주며, 각 함수의 역할과 호출 관계를 파악하는 데 도움이 됩니다.

## 01. 초기 설정 및 모듈 불러오기
* if __name__ == "__main__": 블록이 실행됩니다. 이 블록은 스크립트가 직접 실행될 때만 동작하도록 하는 파이썬의 표준 패턴입니다.
* main() 함수가 호출됩니다.
### 사용된 모듈:
* sounddevice: 시스템 마이크를 제어하여 녹음된 음성을 배열 형태로 받습니다.
* numpy: sounddevice가 전달하는 음성 데이터를 효과적으로 다루는 데 사용됩니다.
* scipy.io.wavfile: numpy 배열 형태의 음성 데이터를 WAV 파일로 저장하는 데 사용됩니다.
* os: 파일 시스템 경로를 다룹니다.
* datetime: 파일명에 날짜와 시간을 포함시키는 데 사용됩니다.
* speech_recognition: Google Speech API를 사용하여 음성을 텍스트로 변환하는 데 사용됩니다.
* pandas: 데이터프레임을 생성하고 CSV 파일로 저장하는 데 사용됩니다. 

## 2. 폴더 생성 및 경로 설정
* CURRENT_FOLDER, RECORDS_FOLDER, CSV_FILE_PATH 변수가 설정됩니다.
* os.path.abspath(__file__)를 사용하여 스크립트의 절대 경로를 가져와 CURRENT_FOLDER에 저장합니다.
* os.path.join()를 사용하여 records 폴더와 all_records.csv 파일의 최종 경로를 구성합니다.
* if not os.path.exists(RECORDS_FOLDER): os.makedirs(RECORDS_FOLDER)를 통해 records 폴더가 존재하지 않으면 새로 생성합니다. 

## 3. 메인 반복문 실행 (main())
* while True: 무한 반복문이 시작됩니다. 이 루프는 사용자가 Ctrl+C를 누르거나 예상치 못한 오류가 발생할 때까지 계속됩니다.
* input() 함수를 사용하여 사용자로부터 Enter 키 입력을 기다립니다.
* 사용자가 Enter 키를 누르면 다음 단계로 진행합니다. 

## 4. 음성 녹음 (record_audio())
* record_audio(duration, fs) 함수가 호출됩니다.
* sounddevice.rec() 함수를 사용하여 5초 동안 마이크에서 음성 데이터를 녹음합니다.
* sounddevice.wait()를 호출하여 녹음이 완료될 때까지 기다립니다.
* 녹음이 완료되면 numpy 배열 형태의 음성 데이터가 반환됩니다. 

## 5. 녹음 파일 저장 (save_recording())
* save_recording(recording, fs) 함수가 호출됩니다.
* recording * np.iinfo(np.int16).max로 float64 녹음 데이터를 16비트 정수형으로 변환합니다. np.iinfo()는 정수형 타입의 최댓값을 제공합니다.
* astype(np.int16)를 사용하여 데이터 타입을 int16으로 변환합니다.
* scipy.io.wavfile.write() 함수를 사용하여 변환된 데이터를 PCM WAV 형식 파일로 저장합니다.
* 저장된 파일의 경로가 반환됩니다. 

## 6. 텍스트 변환 및 CSV 저장 (process_recording())
* process_recording(filename) 함수가 호출됩니다.
* speech_recognition.Recognizer() 객체를 생성합니다.
* sr.AudioFile()로 .wav 파일을 엽니다.
* recognizer.record(source)로 오디오 데이터를 읽습니다.
recognize_google()를 호출하여 Google Speech API로 음성을 텍스트로 변환합니다.
* API 키가 필요 없으며, 음성 데이터가 Google 서버로 전송됩니다.
* 텍스트 변환에 성공하면 save_transcription_as_csv(text) 함수를 호출합니다.
* try...except 블록으로 API 통신 실패나 음성 인식 실패 등 예외를 처리합니다. 

## 7. CSV 파일에 기록 추가 (save_transcription_as_csv())
* save_transcription_as_csv(text) 함수가 호출됩니다.
* 현재 날짜와 시간을 포함한 데이터프레임을 pandas로 생성합니다.
* os.path.exists(CSV_FILE_PATH)로 all_records.csv 파일이 존재하는지 확인합니다.
* 파일이 없으면: to_csv()로 파일을 새로 만들고 헤더를 포함하여 저장합니다.
* 파일이 있으면: mode='a'와 header=False 옵션을 사용하여 기존 파일에 데이터를 추가합니다. 

## 8. 키워드 검색 (search_keyword())
* search_keyword() 함수가 호출됩니다.
* pandas.read_csv()를 사용하여 all_records.csv 파일의 모든 내용을 데이터프레임으로 읽습니다.
* input() 함수로 사용자로부터 검색어를 받습니다.
* isdigit() 메서드로 입력이 숫자인지 문자인지 판별합니다.
* 숫자 검색: astype(str).str.contains()로 '음성 파일내에서의 시간' 열에서 검색합니다.
* 문자 검색: str.replace(' ', '').str.contains()로 '인식된 텍스트' 열에서 공백을 제거한 뒤 검색합니다.
* 검색 결과를 출력하고, 다음 반복을 위해 main() 함수로 돌아갑니다. 

## 9. 프로그램 종료
* 사용자가 Ctrl+C를 누르면 try...except KeyboardInterrupt 블록이 실행됩니다.
* print("\n프로그램을 종료합니다.") 메시지를 출력하고 break 문을 통해 while 루프를 종료합니다.
* 루프가 종료되면 스크립트 실행이 끝납니다.
