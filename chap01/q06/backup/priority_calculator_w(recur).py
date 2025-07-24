# 사칙연산 함수
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a / b

# ✅ 계산기 메인 함수: 괄호 포함 수식 평가
def evaluate(expression):
    expression = expression.replace(" ", "")  # 공백 제거

    def helper(expr, start=0):
        tokens = []
        num = ""
        i = start
        prev = ""

        while i < len(expr):
            char = expr[i]

            if char == "(":
                if num:
                    tokens.append(num)
                    num = ""
                    tokens.append("*")
                elif tokens and (tokens[-1] == ")" or tokens[-1].replace('.', '', 1).lstrip("+-").isdigit()):
                    tokens.append("*")

                val, jump = helper(expr, i + 1)
                tokens.append(str(val))
                i = jump
                prev = ")"
                continue

            elif char == ")":
                if start == 0:
                    raise ValueError("닫는 괄호 ')'에 대응하는 여는 괄호 '('가 없습니다.")
                if num:
                    tokens.append(num)
                    num = ""
                return calculate(tokens), i

            elif char in "0123456789.":
                num += char

            elif char in "+-":
                if i == 0 or prev in "+-*/(":
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
                raise ValueError(f"잘못된 문자: '{char}'")

            prev = char
            i += 1

        if num:
            tokens.append(num)

        if start > 0:
            raise ValueError("괄호가 닫히지 않았습니다.")

        return calculate(tokens), i


    # 최종 결과만 반환
    result, _ = helper(expression)
    return result

# ✅ 연산 우선순위 계산 함수 (곱/나눗셈 → 덧/뺄셈)
def calculate(tokens):
    # 1단계: 곱셈/나눗셈
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

    # 2단계: 덧셈/뺄셈
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

# ✅ 사용자 입력 처리
def main():
    try:
        expression = input("수식을 입력하세요: ")
        result = evaluate(expression)
        print(f"결과: {result}")
    except ZeroDivisionError:
        print("오류: 0으로 나눌 수 없습니다.")
    except Exception as e:
        print(f"잘못된 입력입니다: {e}")

# ✅ 실행 시작점
if __name__ == "__main__":
    main()
