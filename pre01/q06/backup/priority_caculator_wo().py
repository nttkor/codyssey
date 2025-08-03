def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0: raise ZeroDivisionError
    return a / b

# 개선된 tokenizer
def tokenizer(expression):
    expression = expression.replace(" ", "")  # 공백 제거
    tokens = []
    num = ""
    prev = ""  # 이전 문자

    for i, char in enumerate(expression):
        if char in "0123456789.":
            num += char
        elif char in "+-":
            if i == 0 or prev in "+-*/":  # 단항 부호
                num += char
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
        else:
            raise ValueError(f"Invalid character '{char}' in expression.")
        prev = char

    if num:
        tokens.append(num)
    return tokens

# 연산 우선순위를 고려한 계산 함수
def calculate(tokens):
    # 1단계: 곱셈(*)과 나눗셈(/) 먼저 처리
    i = 0
    while i < len(tokens):
        if tokens[i] in ("*", "/"):
            try:
                left = float(tokens[i - 1])
                right = float(tokens[i + 1])

                if tokens[i] == "*":
                    result = multiply(left, right)
                else:
                    result = divide(left, right)

                tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
                i -= 1
            except (ValueError, ZeroDivisionError):
                raise
        else:
            i += 1

    # 2단계: 덧셈(+)과 뺄셈(-)
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

                tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
                i -= 1
            except ValueError:
                raise
        else:
            i += 1

    return float(tokens[0])

# 메인 함수
def main():
    try:
        expression = input("Enter expression: ")
        tokens = tokenizer(expression)
        result = calculate(tokens)
        print(f"Result: {result}")
    except ZeroDivisionError:
        print("Error: Division by zero.")
    except Exception:
        print("Invalid input.")

if __name__ == "__main__":
    main()