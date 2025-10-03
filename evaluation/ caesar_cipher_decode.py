	
# 문제 2. 카이사르 암호
# 수행 과제
# password.txt 파일을 읽어온다.
# 카이사르의 암호를 풀 수 있는 함수를 caesar_cipher_decode() 라는 이름으로 만든다.
# caesar_cipher_decode() 함수는 풀어야 하는 문자열을 파라메터로 추가한다. 이때 파라메터의 이름은 target_text으로 한다.
# caesar_cipher_decode() 에서 자리수에 따라 암호표가 바뀌게 한다. 자리수는 알파벳 수만큼 반복한다.
# 자리수에 따라서 해독된 결과를 출력한다.
# 몇 번째 자리수로 암호가 해독되는지 찾아낸다. 눈으로 식별이 가능하면 해당 번호를 입력하면 그 결과를 result.txt로 저장을 한다.
# 보너스 과제
# 텍스트 사전을 만들고 사전에 있는 단어와 일치하는 키워드가 암호속에서 발견될 경우 반복을 멈출 수 있게 작성해 보시오.

def open_file(path):
    try:
        with open(path,mode='r',encoding='utf-8') as f:
            return f.read()
    except:
        raise
def caesar_cipher_decode(target_text):
    """
    카이사르 암호 해독 함수
    - 주어진 텍스트에 대해 지정한 shift만큼 알파벳을 뒤로 이동시켜 복호화
    - 대소문자 구분하며 알파벳 이외 문자는 변경하지 않음
    """



def main():
    try:
        target_text = open_file('evaluation/password.txt')
        print(target_text)
    except:
        return

if __name__ == '__main__':
    main()