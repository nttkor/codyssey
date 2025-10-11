더 간단한 방법이 있나?
Flask 없이 Python 스크립트만으로 음성 녹음하기
웹 서버(Flask)를 사용하는 것이 복잡하게 느껴진다면, 그래픽 사용자 인터페이스(GUI) 없이 터미널에서 실행하는 파이썬 스크립트만으로 마이크에서 음성을 녹음하고 파일로 저장할 수 있습니다. 
이 방법은 웹 페이지를 만들 필요가 없어서 훨씬 간단합니다. sounddevice와 scipy 라이브러리를 사용합니다.
1단계: 라이브러리 설치하기
VS Code 터미널에서 다음 명령어를 실행하여 필요한 라이브러리를 설치합니다.
bash
pip install sounddevice scipy
코드를 사용할 때는 주의가 필요합니다.

2단계: 음성 녹음 스크립트 작성하기 (javis.py)
javis.py 파일을 생성하고 다음 코드를 작성합니다.
python
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
import datetime
import time

# 녹음 파일 저장 경로 설정
RECORDS_FOLDER = 'records'
if not os.path.exists(RECORDS_FOLDER):
    os.makedirs(RECORDS_FOLDER)

def record_audio(duration, fs):
    """
    지정된 시간(duration) 동안 마이크에서 음성을 녹음합니다.
    """
    print("녹음을 시작합니다. 말씀하세요...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
    sd.wait()  # 녹음이 끝날 때까지 기다립니다.
    print("녹음을 완료했습니다.")
    return recording

def save_recording(recording, fs):
    """
    녹음된 음성 데이터를 wav 파일로 저장합니다.
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = os.path.join(RECORDS_FOLDER, f'{timestamp}.wav')
    write(filename, fs, recording)
    print(f"파일이 저장되었습니다: {filename}")

def main():
    """
    메인 함수: 녹음 시작, 저장 및 반복 실행.
    """
    fs = 44100  # 샘플링 주파수
    duration = 5  # 녹음 시간(초)

    while True:
        try:
            input(f"{duration}초 녹음을 시작하려면 Enter 키를 누르세요. (종료하려면 Ctrl+C)")
            recording = record_audio(duration, fs)
            save_recording(recording, fs)
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")
            break

if __name__ == "__main__":
    main()

코드를 사용할 때는 주의가 필요합니다.

3단계: 스크립트 실행하기
VS Code 터미널에서 다음 명령어를 입력하여 스크립트를 실행합니다.
bash
python javis.py
코드를 사용할 때는 주의가 필요합니다.

Enter 키를 누르면 5초간 녹음이 시작되고, records 폴더에 년월일-시간분초.wav 형식의 파일이 자동으로 저장됩니다.
보너스 과제 (파이썬 스크립트 버전)
특정 날짜 범위의 녹음 파일을 보여주는 기능은 간단한 파이썬 스크립트로 구현할 수 있습니다. javis.py에 다음 함수를 추가합니다.
python
def show_recordings_by_date():
    """
    사용자에게 날짜 범위를 입력받아 해당하는 녹음 파일 목록을 출력합니다.
    """
    start_date_str = input("시작 날짜를 입력하세요 (예: 20251007): ")
    end_date_str = input("종료 날짜를 입력하세요 (예: 20251008): ")

    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d')

        print("\n검색 결과:")
        files = os.listdir(RECORDS_FOLDER)
        for filename in sorted(files):
            if filename.endswith('.wav'):
                file_date_str = filename.split('-')[0]
                file_date = datetime.datetime.strptime(file_date_str, '%Y%m%d')
                if start_date <= file_date <= end_date:
                    print(filename)
    except (ValueError, IndexError):
        print("잘못된 날짜 형식입니다.")

def main():
    fs = 44100
    duration = 5

    while True:
        try:
            choice = input("\n1. 녹음하기\n2. 날짜별 검색하기\n3. 종료\n선택: ")
            if choice == '1':
                input(f"{duration}초 녹음을 시작하려면 Enter 키를 누르세요. ")
                recording = record_audio(duration, fs)
                save_recording(recording, fs)
            elif choice == '2':
                show_recordings_by_date()
            elif choice == '3':
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")
            break

if __name__ == "__main__":
    main()
코드를 사용할 때는 주의가 필요합니다.

AI 대답에는 오류가 있을 수 있습니다. 자세히 알아보기