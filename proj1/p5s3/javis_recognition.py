# -*- coding: utf-8 -*-

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
import datetime
import time
import speech_recognition as sr
import pandas as pd


# 녹음 파일 저장 경로 설정
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
RECORDS_FOLDER_NAME = 'records'
RECORDS_FOLDER = os.path.join(CURRENT_FOLDER, RECORDS_FOLDER_NAME)

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
    녹음된 음성 데이터를 16비트 PCM wav 파일로 저장하고, 저장된 파일 경로를 반환합니다.
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = os.path.join(RECORDS_FOLDER, f'{timestamp}.wav')
    
    # 1. -1.0 ~ 1.0 범위의 float64 데이터를 -32768 ~ 32767 범위의 int16으로 변환
    #    (np.iinfo(np.int16).max = 32767)
    recording_int16 = (recording * np.iinfo(np.int16).max).astype(np.int16)
    
    # 2. 16비트 정수형 PCM 데이터로 저장
    write(filename, fs, recording_int16)
    
    print(f"파일이 저장되었습니다: {filename}")
    return filename # 파일 경로 반환 추가



def save_transcription_as_csv(filename, text):
    """
    STT 결과를 CSV 파일로 저장합니다.
    """
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    csv_filename = os.path.join(RECORDS_FOLDER, f'{base_filename}.csv')

    df = pd.DataFrame([{'음성 파일내에서의 시간': '0', '인식된 텍스트': text}])
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"STT 결과가 CSV 파일로 저장되었습니다: {csv_filename}")


def process_recording(filename):
    """
    녹음된 파일을 STT로 변환하고 CSV로 저장합니다.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio_data = recognizer.record(source)
            print("음성을 텍스트로 변환 중...")
            text = recognizer.recognize_google(audio_data, language='ko-KR')
            print(f"인식된 텍스트: {text}")
            save_transcription_as_csv(filename, text)

    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print(f"Google Web Speech API 서비스에서 에러가 발생했습니다: {e}")
# javis.py 파일에 다음 함수 추가

def search_csv_for_keyword(keyword, folder=RECORDS_FOLDER):
    """
    지정된 키워드가 포함된 CSV 파일을 찾아 해당 내용을 출력합니다.
    """
    found_count = 0
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder, filename)
            try:
                df = pd.read_csv(file_path)
                # '인식된 텍스트' 열에 키워드가 포함된 행 찾기
                if not df[df['인식된 텍스트'].str.contains(keyword, case=False, na=False)].empty:
                    print(f"\n파일 '{filename}'에서 키워드 '{keyword}'를 찾았습니다.")
                    print(df)
                    found_count += 1
            except Exception as e:
                print(f"파일 '{filename}' 처리 중 오류 발생: {e}")
    
    if found_count == 0:
        print(f"\n키워드 '{keyword}'를 포함하는 파일을 찾을 수 없습니다.")


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
            filename = save_recording(recording, fs)

            if filename:
                process_recording(filename)

        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")
            break


if __name__ == "__main__":
    main()
