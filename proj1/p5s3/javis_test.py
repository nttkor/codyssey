# 1단계: 라이브러리 설치하기
# VS Code 터미널에서 다음 명령어를 실행하여 필요한 라이브러리를 설치합니다.
# bash
# pip install sounddevice scipy
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
