# 덧셈 함수
def add(a, b):
    return a + b

# 뺄셈 함수
def subtract(a, b):
    return a - b

# 곱셈 함수
def multiply(a, b):
    return a * b

# 나눗셈 함수 (0으로 나눌 경우 예외 발생)
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a / b

def tokenizer(expression):
    expression = list(expression.replace(" ", ""))  # 공백 제거
    tokens = []
    operand = ""
    operator = ""

    for i, v in enumerate(expression):
        if operand == '':
            if v in '01234567890-+':
                operand = v
            else:
                raise ValueError(f"Invalid character '{v}' in expression.")
        elif v in '01234567890.':
            operand += v
        elif v in '+-*/':
            tokens.append(operand)
            operand = ""
            tokens.append(v)
        else:
            raise ValueError(f"Invalid character '{v}' in expression.")
    return tokens + [operand] if operand else tokens


# 연산 우선순위를 고려한 계산 함수
def calculate(tokens):
    # 1단계: 곱셈(*)과 나눗셈(/) 먼저 처리
    i = 0
    while i < len(tokens):
        if tokens[i] in ("*", "/"):
            try:
                left = float(tokens[i - 1])   # 왼쪽 피연산자
                right = float(tokens[i + 1])  # 오른쪽 피연산자

                if tokens[i] == "*":
                    result = multiply(left, right)
                else:
                    result = divide(left, right)

                # 계산된 결과를 기준으로 토큰 리스트를 갱신
                tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
                i -= 1  # 리스트가 줄었으므로 인덱스 조정
            except (ValueError, ZeroDivisionError):
                raise
        else:
            i += 1

    # 2단계: 덧셈(+)과 뺄셈(-) 처리
    i = 0
    while i < len(tokens):
        if tokens[i] in ("+", "-"):
            try:
                left = float(tokens[i - 1])
                right = float(tokens[i + 1])

                if tokens[i] == "+":
                    result = add(left, right)
                else:
                    result = subtract(left, right)

                # 계산된 결과를 기준으로 토큰 리스트를 갱신
                tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
                i -= 1
            except ValueError:
                raise
        else:
            i += 1

    # 최종 결과 반환
    return float(tokens[0])

# 메인 함수
def main():
    try:
        # 사용자로부터 수식 입력 받기
        expression = input("Enter expression: ")
        
        tokens = tokenizer(expression)  # 공백으로 토큰화

        # 토큰 수가 올바르지 않으면 오류 발생
        if len(tokens) < 3 or len(tokens) % 2 == 0:
            raise ValueError("Invalid token count.")

        # 피연산자(짝수 인덱스)와 연산자(홀수 인덱스) 검증
        for i, token in enumerate(tokens):
            if i % 2 == 0:
                float(token)  # 피연산자가 숫자인지 확인
            else:
                if token not in ("+", "-", "*", "/"):
                    raise ValueError("Invalid operator.")

        # 계산 수행
        result = calculate(tokens)
        print(f"Result: {result}")

    # 0으로 나누는 경우 예외 처리
    except ZeroDivisionError:
        print("Error: Division by zero.")

    # 그 외의 모든 잘못된 입력에 대한 처리
    except Exception:
        print("Invalid input.")

# 프로그램의 시작점
if __name__ == "__main__":
    main()
