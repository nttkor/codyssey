import re

# 사칙연산 함수
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다.")
    return a / b

# ✅ 괄호 없이 일반 수식 토크나이징 (생략 곱셈, 음수 포함)
def tokenize(expression):
    tokens = []
    num = ""
    prev = ""
    
    for i, char in enumerate(expression):
        if char in "0123456789.":
            num += char
        elif char in "+-":
            if i == 0 or prev in "+-*/(":
                num += char  # 단항 부호
            else:
                if num:
                    tokens.append(num)
                    num = ""
                tokens.append(char)
        elif char in "*/":
            if num:
                tokens.append(num)
                num = ""
            tokens.append(char)
        elif char == "(":
            if num:  # 생략된 곱셈 (예: 2(3+1))
                tokens.append(num)
                tokens.append("*")
                num = ""
            tokens.append(char)
        elif char == ")":
            if num:
                tokens.append(num)
                num = ""
            tokens.append(char)
        else:
            raise ValueError(f"잘못된 문자: '{char}'")
        prev = char

    if num:
        tokens.append(num)

    return tokens

# ✅ 괄호 없는 토큰 계산 (우선순위 고려)
def calculate(tokens):
    # 곱셈/나눗셈 먼저
    i = 0
    while i < len(tokens):
        if tokens[i] in ("*", "/"):
            left = float(tokens[i - 1])
            right = float(tokens[i + 1])
            result = multiply(left, right) if tokens[i] == "*" else divide(left, right)
            tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
            i -= 1
        else:
            i += 1

    # 덧셈/뺄셈
    i = 0
    while i < len(tokens):
        if tokens[i] in ("+", "-"):
            left = float(tokens[i - 1])
            right = float(tokens[i + 1])
            result = add(left, right) if tokens[i] == "+" else subtract(left, right)
            tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
            i -= 1
        else:
            i += 1

    return float(tokens[0])

# ✅ 전체 수식 평가: 괄호 전개 + 계산
def evaluate(expression):
    expression = expression.replace(" ", "")  # 공백 제거

    # 괄호 짝 검사용 스택
    stack = []
    for char in expression:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if not stack:
                raise ValueError("닫는 괄호 ')'에 대응하는 여는 괄호 '('가 없습니다.")
            stack.pop()
    if stack:
        raise ValueError("괄호가 닫히지 않았습니다.")

    # 괄호 전개 처리
    while "(" in expression:
        # 가장 안쪽 괄호부터 찾아 계산
        inner_exprs = re.findall(r'\([^()]*\)', expression)
        for inner in inner_exprs:
            val = evaluate(inner[1:-1])  # 괄호 안만 재귀 호출
            expression = expression.replace(inner, str(val), 1)

    # 괄호 없는 수식을 토크나이즈하고 계산
    tokens = tokenize(expression)
    return calculate(tokens)

# ✅ 메인 함수
def main():
    try:
        expr = input("수식을 입력하세요: ")
        result = evaluate(expr)
        print(f"결과: {result}")
    except ZeroDivisionError as zde:
        print("오류:", zde)
    except Exception as e:
        print("잘못된 입력입니다:", e)

# ✅ 시작점
if __name__ == "__main__":
    main()
