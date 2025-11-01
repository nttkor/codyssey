import sqlite3  # SQLite 데이터베이스를 사용하기 위한 모듈
import os  # 파일 경로 및 디렉토리 제어를 위한 모듈

os.chdir(os.path.dirname(__file__))  # 현재 파일이 위치한 디렉토리로 작업 디렉토리 변경

def create_table():  # 데이터베이스 테이블을 생성하는 함수 정의
    conn = sqlite3.connect("smartfarm.db")  # smartfarm.db 파일에 연결 (없으면 자동 생성)
    cursor = conn.cursor()  # SQL 실행을 위한 커서 객체 생성
    cursor.execute("""  # 테이블 생성 SQL 실행
        CREATE TABLE IF NOT EXISTS parm_data (  # 테이블이 없을 경우에만 생성
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # 자동 증가하는 고유 ID (기본 키)
            sensor_name TEXT,  # 센서 이름 (문자열)
            timestamp DATETIME,  # 데이터 입력 시간
            temperature INTEGER,  # 온도 (정수)
            light INTEGER,  # 조도 (정수)
            humidity INTEGER  # 습도 (정수)
        )
    """)  # SQL 문 끝
    conn.commit()  # 변경사항 저장
    conn.close()  # 데이터베이스 연결 종료

if __name__ == '__main__':  # 이 파일이 직접 실행될 경우
    create_table()  # 테이블 생성 함수 호출
    print("✅ 데이터베이스와 테이블이 준비되었습니다.")  # 완료 메시지 출력
