import sys
import time

def print_status(total_count, last_passwords):
    last_line_length = 0
    try:
        while True:
            current_time = time.strftime("%H:%M:%S")
            # 출력할 문장: 시간만 바뀜, 나머지는 고정
            line = f"시간: {current_time} | 총 시도 개수: {total_count} | 마지막 암호들: {', '.join(last_passwords)}"
            
            # 이전 출력보다 짧으면 공백으로 덮어줌
            if len(line) < last_line_length:
                line += ' ' * (last_line_length - len(line))
            else:
                last_line_length = len(line)

            sys.stdout.write('\r' + line)
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n프로그램 종료")

if __name__ == "__main__":
    # 예시 고정값 (원래는 실시간 업데이트 값)
    total_count = 21000
    last_passwords = ['abcxyz', 'def123', 'ghi456', 'jkl789', 'mno012', 'pqr345']

    print_status(total_count, last_passwords)
