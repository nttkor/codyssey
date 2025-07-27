# 사칙연산 함수 정의
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError  # 0으로 나누면 예외 발생
    return a / b

# 연산자 우선순위 설정
precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

# ✅ 수식을 토큰화하는 함수 (괄호, 음수, 생략 곱셈까지 지원)
def tokenizer(expression):
    expression = expression.replace(" ", "")  # 공백 제거
    tokens = []     # 최종 토큰 리스트
    num = ""        # 숫자 임시 저장
    prev = ""       # 직전 문자

    i = 0
    while i < len(expression):
        char = expression[i]

        # 숫자 및 소수점 처리
        if char in "0123456789.":
            num += char

        # + 또는 - 부호 처리 (단항/이항 구분)
        elif char in "+-":
            if i == 0 or prev in "()+-*/":  # 단항 부호로 판단
                num += char
            else:
                if num:
                    tokens.append(num)
                    num = ""
                tokens.append(char)

        # 곱셈/나눗셈 연산자
        elif char in "*/":
            if num:
                tokens.append(num)
                num = ""
            tokens.append(char)

        # 여는 괄호 처리
        elif char == "(":
            if num:  # 숫자 바로 뒤 괄호: 생략된 곱셈 처리 (예: 2(3+1) → 2 * (3+1))
                tokens.append(num)
                num = ""
                tokens.append("*")
            tokens.append(char)

        # 닫는 괄호 처리
        elif char == ")":
            if num:
                tokens.append(num)
                num = ""
            tokens.append(char)

        else:
            raise ValueError(f"잘못된 문자: '{char}'")

        prev = char
        i += 1

    # 마지막 숫자 처리
    if num:
        tokens.append(num)

    return tokens

# ✅ 중위 표기식 → 후위 표기식 변환 함수 (Shunting Yard 알고리즘)
def to_postfix(tokens):
    output = []  # 출력(후위 표기 리스트)
    stack = []   # 연산자 스택

    for token in tokens:
        # 숫자인 경우 (양수, 음수 포함)
        if token.replace('.', '', 1).lstrip("+-").isdigit():
            output.append(token)

        # 연산자인 경우
        elif token in precedence:
            while stack and stack[-1] in precedence and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)

        # 여는 괄호
        elif token == "(":
            stack.append(token)

        # 닫는 괄호
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack or stack[-1] != "(":
                raise ValueError("괄호가 맞지 않습니다.")
            stack.pop()  # 여는 괄호 제거

        else:
            raise ValueError(f"잘못된 토큰: '{token}'")

    # 남은 연산자 모두 출력으로 이동
    while stack:
        if stack[-1] in "()":
            raise ValueError("괄호가 맞지 않습니다.")
        output.append(stack.pop())

    return output

# ✅ 후위 표기식 계산 함수
def evaluate_postfix(postfix):
    stack = []
    for token in postfix:
        if token in precedence:
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(add(a, b))
            elif token == "-":
                stack.append(subtract(a, b))
            elif token == "*":
                stack.append(multiply(a, b))
            elif token == "/":
                stack.append(divide(a, b))
        else:
            stack.append(float(token))
    return stack[0]

# ✅ 메인 함수
def main():
    try:
        expression = input("수식을 입력하세요: ")
        tokens = tokenizer(expression)
        postfix = to_postfix(tokens)
        result = evaluate_postfix(postfix)
        print(f"결과: {result}")
    except ZeroDivisionError:
        print("오류: 0으로 나눌 수 없습니다.")
    except Exception as e:
        print(f"잘못된 입력입니다: {e}")

# 프로그램 실행 시작점
if __name__ == "__main__":
    main()
