# -*- coding: utf-8 -*- # 한글 주석을 위한 인코딩 명시

import sounddevice as sd    # 마이크를 통해 음성을 녹음하기 위한 라이브러리
import numpy as np          # 음성 데이터를 배열로 다루기 위한 라이브러리
from scipy.io.wavfile import write # 녹음된 데이터를 WAV 파일로 저장하기 위한 라이브러리
import os                   # 파일 경로와 관련된 작업을 위한 라이브러리
import datetime             # 파일명에 날짜와 시간을 포함하기 위한 라이브러리
import time                 # 시간 관련 작업을 위한 라이브러리 (현재는 사용하지 않음)
import speech_recognition as sr # 음성을 텍스트로 변환하기 위한 라이브러리 (Google API 사용)
import pandas as pd         # 데이터를 표 형태로 다루고 CSV 파일로 저장/읽기 위한 라이브러리


# 녹음 파일 저장 경로 설정
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__)) # 현재 스크립트의 절대 경로
RECORDS_FOLDER_NAME = 'records'                         # 녹음 파일을 저장할 폴더 이름
RECORDS_FOLDER = os.path.join(CURRENT_FOLDER, RECORDS_FOLDER_NAME) # 전체 저장 경로
CSV_FILE_PATH = os.path.join(RECORDS_FOLDER, 'all_records.csv') # 모든 기록을 저장할 CSV 파일 경로

if not os.path.exists(RECORDS_FOLDER):  # records 폴더가 없으면
    os.makedirs(RECORDS_FOLDER)         # 폴더 생성


def record_audio(duration, fs): # 녹음 시간(duration)과 샘플링 주파수(fs)를 인자로 받음
    """
    지정된 시간(duration) 동안 마이크에서 음성을 녹음합니다.
    """
    print("녹음을 시작합니다. 말씀하세요...")                     # 사용자에게 녹음 시작 알림
    # 지정된 시간, 주파수, 채널, 데이터 타입으로 녹음 시작
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
    sd.wait()                                                   # 녹음이 끝날 때까지 기다림
    print("녹음을 완료했습니다.")                               # 녹음 완료 알림
    return recording                                            # 녹음된 데이터를 반환


def save_recording(recording, fs): # 녹음 데이터와 샘플링 주파수를 인자로 받음
    """
    녹음된 음성 데이터를 16비트 PCM wav 파일로 저장하고, 저장된 파일 경로를 반환합니다.
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') # 현재 시간을 '년월일-시간분초' 형식으로 포맷
    filename = os.path.join(RECORDS_FOLDER, f'{timestamp}.wav')   # 파일 경로 생성

    # 1. -1.0 ~ 1.0 범위의 float64 데이터를 -32768 ~ 32767 범위의 int16으로 변환
    recording_int16 = (recording * np.iinfo(np.int16).max).astype(np.int16)

    # 2. 16비트 정수형 PCM 데이터로 저장
    write(filename, fs, recording_int16)

    print(f"음성 파일이 저장되었습니다: {filename}")            # 저장된 파일 경로 출력
    return filename                                             # 파일 경로 반환


def save_transcription_as_csv(text):    # 인식된 텍스트를 인자로 받음
    """
    STT 결과를 하나의 CSV 파일에 추가합니다.
    """
    timestamp_str = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') # 현재 시간을 '년월일-시간분초' 형식으로 포맷

    # 새로운 데이터프레임 생성
    new_data = pd.DataFrame([{'음성 파일내에서의 시간': timestamp_str, '인식된 텍스트': text}])

    if not os.path.exists(CSV_FILE_PATH):   # CSV 파일이 없으면
        new_data.to_csv(CSV_FILE_PATH, index=False, encoding='utf-8-sig') # 헤더와 함께 파일 생성
    else:                                   # CSV 파일이 있으면
        new_data.to_csv(CSV_FILE_PATH, mode='a', index=False, header=False, encoding='utf-8-sig') # 헤더 없이 데이터만 추가

    print(f"STT 결과가 '{os.path.basename(CSV_FILE_PATH)}' 파일에 추가되었습니다.")


def process_recording(filename):    # 녹음된 파일명을 인자로 받음
    """
    녹음된 파일을 STT로 변환하고, 결과를 CSV에 추가합니다.
    """
    recognizer = sr.Recognizer()    # SpeechRecognition 객체 생성
    try:
        with sr.AudioFile(filename) as source: # WAV 파일 열기
            audio_data = recognizer.record(source) # 파일의 모든 오디오 데이터 읽기
            print("음성을 텍스트로 변환 중...")
            text = recognizer.recognize_google(audio_data, language='ko-KR') # Google API로 텍스트 변환
            print(f"인식된 텍스트: {text}")

            save_transcription_as_csv(text) # CSV 파일에 텍스트 저장

    except sr.UnknownValueError:    # 음성 인식이 실패한 경우
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:    # API 요청 실패한 경우
        print(f"Google Web Speech API 서비스에서 에러가 발생했습니다: {e}")


def search_keyword(): # 키워드 검색 기능
    """
    사용자로부터 키워드를 입력받아 CSV 파일에서 해당 기록을 찾아 출력합니다.
    입력된 값이 숫자이면 시간 열을, 문자이면 텍스트 열을 검색합니다.
    검색 시에는 공백을 제거한 후 비교합니다.
    """
    if not os.path.exists(CSV_FILE_PATH):   # CSV 파일이 없으면
        print("검색할 기록 파일이 없습니다.")
        return

    try:
        df = pd.read_csv(CSV_FILE_PATH)     # CSV 파일 읽어오기
        print("\n--- 전체 기록 ---")
        print(df)                           # 전체 기록 출력

        keyword = input("\n찾고 싶은 단어나 숫자를 입력하세요: ").strip() # 사용자 입력
        if not keyword:                     # 입력이 없으면
            print("입력이 없어 검색을 건너뜁니다.")
            return

        is_numeric = keyword.isdigit()      # 입력이 숫자인지 확인
        matches = pd.DataFrame()            # 결과를 저장할 빈 데이터프레임

        cleaned_keyword = keyword.replace(' ', '') # 검색어의 공백 제거

        if is_numeric:  # 입력이 숫자일 경우
            matches = df[df['음성 파일내에서의 시간'].astype(str).str.contains(cleaned_keyword, na=False)]
        else:           # 입력이 문자일 경우
            # '인식된 텍스트' 열의 공백 제거 후 검색
            matches = df[df['인식된 텍스트'].str.replace(' ', '').str.contains(cleaned_keyword, case=False, na=False)]

        if not matches.empty:   # 검색 결과가 있으면
            print(f"\n--- '{keyword}'(으)로 검색된 기록 ---")
            for index, row in matches.iterrows(): # 모든 검색 결과 출력
                print(f"날짜: {row['음성 파일내에서의 시간']} | 내용: {row['인식된 텍스트']}")
        else:                   # 검색 결과가 없으면
            print(f"'{keyword}'가 포함된 기록을 찾을 수 없습니다.")

    except Exception as e:      # 예외 발생 시
        print(f"검색 중 오류가 발생했습니다: {e}")


def main():                     # 메인 함수
    """
    메인 함수: 녹음 시작, 저장, STT, CSV 처리, 키워드 검색을 반복 실행.
    """
    fs = 44100                  # 샘플링 주파수 설정
    duration = 5                # 녹음 시간(초) 설정

    while True:                 # 무한 반복
        try:
            input(f"{duration}초 녹음을 시작하려면 Enter 키를 누르세요. (종료하려면 Ctrl+C)") # 사용자 입력 대기
            recording = record_audio(duration, fs)      # 녹음 시작
            filename = save_recording(recording, fs)    # 녹음 파일 저장

            if filename:                                # 녹음 파일이 성공적으로 저장되면
                process_recording(filename)             # STT 및 CSV 저장
                
            search_keyword()                            # 키워드 검색 기능 실행

        except KeyboardInterrupt:                       # Ctrl+C 입력 시
            print("\n프로그램을 종료합니다.")
            break                                       # 루프 종료
        except Exception as e:                          # 기타 예외 발생 시
            print(f"오류가 발생했습니다: {e}")
            break                                       # 루프 종료


if __name__ == "__main__":      # 스크립트가 직접 실행될 때만 main 함수 호출
    main()


