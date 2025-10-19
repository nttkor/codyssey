# -*- coding: utf-8 -*-

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
import datetime
import time
import speech_recognition as sr
import pandas as pd
from datetime import date # 날짜 범위 검색을 위해 추가

# 녹음 파일 저장 경로 설정
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
RECORDS_FOLDER_NAME = 'records'
RECORDS_FOLDER = os.path.join(CURRENT_FOLDER, RECORDS_FOLDER_NAME)

# records 폴더가 없으면 생성
if not os.path.exists(RECORDS_FOLDER):
    os.makedirs(RECORDS_FOLDER)


def record_audio(duration, fs):
    """
    지정된 시간(duration) 동안 마이크에서 음성을 녹음합니다.
    """
    print("\n[🎙️ 녹음 시작] 말씀하세요...")
    # 녹음 중임을 사용자에게 알리기 위해 잠시 멈춤
    time.sleep(0.5) 
    # 마이크 인식 및 녹음
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
    sd.wait()  # 녹음이 끝날 때까지 기다립니다.
    print("[✅ 녹음 완료]")
    return recording


def save_recording(recording, fs):
    """
    녹음된 음성 데이터를 16비트 PCM wav 파일로 저장하고, 저장된 파일 경로를 반환합니다.
    파일 이름은 '년월일-시간분초.wav' 형식입니다.
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = os.path.join(RECORDS_FOLDER, f'{timestamp}.wav')
    
    # 1. -1.0 ~ 1.0 범위의 float64 데이터를 -32768 ~ 32767 범위의 int16으로 변환
    recording_int16 = (recording * np.iinfo(np.int16).max).astype(np.int16)
    
    # 2. 16비트 정수형 PCM 데이터로 저장
    write(filename, fs, recording_int16)
    
    print(f"[📂 파일 저장] 파일이 저장되었습니다: {filename}")
    return filename # 파일 경로 반환


def save_transcription_as_csv(filename, text):
    """
    STT 결과를 CSV 파일로 저장합니다.
    """
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    csv_filename = os.path.join(RECORDS_FOLDER, f'{base_filename}.csv')

    # 단일 인식 결과이므로 Time 스탬프는 '0'으로 설정
    df = pd.DataFrame([{'음성 파일내에서의 시간': '0', '인식된 텍스트': text}])
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"[📝 STT 저장] STT 결과가 CSV 파일로 저장되었습니다: {csv_filename}")


def process_recording(filename):
    """
    녹음된 파일을 STT로 변환하고 CSV로 저장합니다.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            # 녹음 파일 전체를 읽어들임
            audio_data = recognizer.record(source) 
            print("[🔄 STT 변환 중...]")
            # Google Speech Recognition API를 사용하여 한국어(ko-KR)로 텍스트 변환
            text = recognizer.recognize_google(audio_data, language='ko-KR')
            print(f"[💬 인식 결과]: {text}")
            save_transcription_as_csv(filename, text)

    except sr.UnknownValueError:
        print("[⚠️ 오류] 음성을 인식할 수 없습니다. 다시 시도해 주세요.")
    except sr.RequestError as e:
        print(f"[⚠️ 오류] Google Web Speech API 서비스에서 에러가 발생했습니다: {e}")
    except Exception as e:
        print(f"[⚠️ 오류] 녹음 처리 중 예상치 못한 오류 발생: {e}")

# 보너스 과제 구현
def display_records_by_date():
    """
    사용자로부터 시작 및 종료 날짜를 입력받아, 해당 기간 내의 녹음 파일(.wav) 목록을 출력합니다.
    """
    print("\n--- [날짜별 녹음 파일 검색] ---")
    
    while True:
        try:
            start_date_str = input("시작 날짜 (YYYYMMDD 형식, 예: 20251001): ")
            end_date_str = input("종료 날짜 (YYYYMMDD 형식, 예: 20251031): ")
            
            # 문자열을 datetime.date 객체로 변환
            start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d').date()
            
            if start_date > end_date:
                print("[⚠️ 오류] 시작 날짜가 종료 날짜보다 늦을 수 없습니다. 다시 입력해 주세요.")
                continue

            break # 날짜 입력 성공 시 루프 탈출
            
        except ValueError:
            print("[⚠️ 오류] 날짜 형식이 올바르지 않습니다. YYYYMMDD 형식으로 입력해 주세요.")
    
    print(f"\n[🔍 검색 중]: {start_date_str}부터 {end_date_str}까지의 녹음 파일")
    
    found_files = []
    
    # records 폴더 내의 모든 파일 순회
    for filename in os.listdir(RECORDS_FOLDER):
        if filename.endswith('.wav'):
            # 파일 이름에서 날짜 부분(예: 20251019) 추출
            # 파일 이름 형식: YYYYMMDD-HHMMSS.wav
            try:
                file_date_str = filename[:8] # YYYYMMDD 추출
                file_date = datetime.datetime.strptime(file_date_str, '%Y%m%d').date()
                
                # 파일의 날짜가 검색 범위 내에 있는지 확인 (시작일 <= 파일 날짜 <= 종료일)
                if start_date <= file_date <= end_date:
                    found_files.append(filename)
            except ValueError:
                # 파일 이름이 형식을 따르지 않는 경우 (무시)
                continue

    if found_files:
        print(f"\n[✅ 검색 결과] 총 {len(found_files)}개의 파일이 발견되었습니다:")
        for file in sorted(found_files):
            print(f"  - {file}")
    else:
        print("[❌ 결과 없음] 해당 날짜 범위 내의 녹음 파일(.wav)을 찾을 수 없습니다.")


def main():
    """
    메인 함수: 녹음/처리 및 파일 검색 기능 선택 메뉴를 제공합니다.
    """
    fs = 44100  # 샘플링 주파수
    duration = 5  # 기본 녹음 시간(초)

    print("--- 🎙️ JAVIS 음성 처리 시스템 시작 ---")
    print(f"저장 폴더: {RECORDS_FOLDER}")
    print(f"기본 녹음 시간: {duration}초\n")

    while True:
        print("\n--- [메인 메뉴] ---")
        print("1. 🎤 음성 녹음 시작 (STT 자동 저장)")
        print("2. 🔍 날짜별 녹음 파일 검색 (보너스 과제)")
        print("3. ❌ 프로그램 종료")
        
        choice = input("선택: ").strip()

        try:
            if choice == '1':
                # 녹음 및 처리 실행
                input(f"\n[1. 녹음 시작] {duration}초 녹음을 시작하려면 Enter 키를 누르세요...")
                recording = record_audio(duration, fs)
                filename = save_recording(recording, fs)

                if filename:
                    process_recording(filename)
                
            elif choice == '2':
                # 날짜별 검색 기능 실행 (보너스 과제)
                display_records_by_date()
                
            elif choice == '3':
                # 프로그램 종료
                print("\n[👋 종료] 프로그램을 종료합니다.")
                break
                
            else:
                print("[⚠️ 오류] 잘못된 선택입니다. 1, 2, 또는 3을 입력해 주세요.")
                
        except KeyboardInterrupt:
            print("\n[👋 종료] 프로그램이 사용자 요청으로 종료됩니다.")
            break
        except Exception as e:
            print(f"\n[🚨 치명적 오류] 프로그램 실행 중 예상치 못한 오류 발생: {e}")
            break


if __name__ == "__main__":
    main()