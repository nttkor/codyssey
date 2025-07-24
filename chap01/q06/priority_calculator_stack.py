# ✅ 사칙연산 함수 정의
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다.")
    return a / b


# ✅ 수식을 숫자와 연산자로 나누는 토크나이저
def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        char = expression[i]

        # 단항 부호 처리
        if char in '+-':
            if i == 0 or expression[i - 1] in '+-*/':   #맨앞이나 문자 앞이 연산자면 숫자로취급
                num = char
                i += 1
                #연속된 숫자 처리
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                try:
                    float(num)  # 이 시점에서 검증
                except ValueError:
                    raise ValueError(f"잘못된 숫자 형식입니다: {num}")
                tokens.append(num)
                continue
            else:
                tokens.append(char)
                i += 1
                continue

        # 숫자 처리
        elif char.isdigit() or char == '.':
            num = char
            i += 1
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num += expression[i]
                i += 1
            try:
                float(num)  # 이 시점에서 검증
            except ValueError:
                raise ValueError(f"잘못된 숫자 형식입니다: {num}")
            tokens.append(num)
            continue

        # 연산자 처리 (괄호는 이 시점에 없음)
        elif char in '*/':
            tokens.append(char)
            i += 1
            continue
        else:
            raise ValueError(f"잘못된 문자: '{char}'")
    return tokens


# ✅ 연산 우선순위를 고려하여 토큰 계산
def calculate(tokens):
    # 곱셈 / 나눗셈 먼저
    i = 0
    while i < len(tokens):
        if tokens[i] in ('*', '/'):
            left = float(tokens[i - 1])
            right = float(tokens[i + 1])
            result = multiply(left, right) if tokens[i] == '*' else divide(left, right)
            tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
            i -= 1
        else:
            i += 1

    # 덧셈 / 뺄셈
    i = 0
    while i < len(tokens):
        if tokens[i] in ('+', '-'):
            left = float(tokens[i - 1])
            right = float(tokens[i + 1])
            result = add(left, right) if tokens[i] == '+' else subtract(left, right)
            tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
            i -= 1
        else:
            i += 1

    return float(tokens[0])


# ✅ 괄호 처리 포함한 메인 평가 함수 (재귀 없음, 스택 기반)
def evaluate(expression):
    expression = expression.replace(" ", "")  # 공백 제거

    # 괄호 짝 검사
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                raise ValueError("닫는 괄호 ')'에 대응하는 여는 괄호 '('가 없습니다.")
            stack.pop()
    if stack:
        raise ValueError("괄호가 닫히지 않았습니다.")

    # 괄호 처리 반복
    while '(' in expression:
        open_stack = []
        for i, char in enumerate(expression):
            if char == '(':
                open_stack.append(i)
            elif char == ')':
                start = open_stack.pop()
                end = i

                inner = expression[start + 1:end]
                value = calculate(tokenize(inner))

                before = expression[:start]
                after = expression[end + 1:]

                # 생략 곱셈 처리
                if before and (before[-1].isdigit() or before[-1] == ')'):
                    before += '*'
                if after and (after[0].isdigit() or after[0] == '('):
                    value = f"{value}*"
                
                #위치 재배치
                expression = before + str(value) + after
                break  # 가장 안쪽 괄호 한 쌍만 처리

    tokens = tokenize(expression)  #괄호가 풀린 상태
    return calculate(tokens)


# ✅ 메인 함수
def main():
    try:
        expr = input("수식을 입력하세요: ")
        result = evaluate(expr)
        print(f"result:{result}")
    except ZeroDivisionError as zde:
        print("오류:", zde)
    except Exception as e:
        print("잘못된 입력입니다:", e)


# ✅ 실행
if __name__ == "__main__":
    main()
