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
        raise ZeroDivisionError("0으로 나눌 수 없습니다.")
    return a / b

def tokenizer(expression):
    expression = expression.replace(" ", "")  # 공백 제거
    tokens = []
    i = 0
    while i < len(expression):
        char = expression[i]
        if char == '(' or char == ')':
            tokens.append(char)
            i += 1
        elif char.isdigit() or (char == '-' and (i == 0 or expression[i-1] in '(*+/-')): # 숫자 또는 음수 부호
            start = i
            # 숫자 (정수 및 소수점 포함)
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                i += 1
            tokens.append(expression[start:i])
        elif char in '+-*/':
            tokens.append(char)
            i += 1
        else:
            raise ValueError(f"'{char}'은(는) 유효하지 않은 문자입니다.")
    return tokens

# 연산 우선순위를 고려한 계산 함수
def calculate(tokens):
    # 단일 숫자로만 이루어진 경우 처리
    if len(tokens) == 1 and isinstance(tokens[0], (int, float, str)):
        return float(tokens[0])
    
    # 1단계: 곱셈(*)과 나눗셈(/) 먼저 처리
    new_tokens = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "*":
            left = float(new_tokens.pop())
            right = float(tokens[i + 1])
            new_tokens.append(multiply(left, right))
            i += 2
        elif tokens[i] == "/":
            left = float(new_tokens.pop())
            right = float(tokens[i + 1])
            new_tokens.append(divide(left, right))
            i += 2
        else:
            new_tokens.append(tokens[i])
            i += 1
    tokens = new_tokens

    # 2단계: 덧셈(+)과 뺄셈(-) 처리
    result = float(tokens[0])
    i = 1
    while i < len(tokens):
        if tokens[i] == "+":
            result = add(result, float(tokens[i + 1]))
        elif tokens[i] == "-":
            result = subtract(result, float(tokens[i + 1]))
        i += 2
    
    return result

# 괄호를 재귀적으로 처리하고 수식을 파싱하는 함수
def parse_expression(tokens):
    # 이 함수는 수식의 현재 부분을 계산하고 닫는 괄호나 수식의 끝을 만날 때까지 진행합니다.
    # 예: "1 + (2 * 3) - 4" 에서 "(2 * 3)" 부분을 처리합니다.

    parsed_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            # 재귀 호출: 괄호 안의 수식을 처리
            sub_result, end_index = parse_expression(tokens[i + 1:])
            parsed_tokens.append(str(sub_result)) # 계산된 결과를 문자열로 추가
            i += end_index + 1 # 닫는 괄호까지 스킵
        elif token == ')':
            # 닫는 괄호를 만나면 현재까지 파싱된 토큰들을 계산하고 결과를 반환
            return calculate(parsed_tokens), i + 1
        else:
            parsed_tokens.append(token)
        i += 1
    
    # 수식의 끝에 도달했을 때 남은 토큰들을 계산
    return calculate(parsed_tokens), i

# 메인 함수
def main():
    try:
        expression = input("Enter expression: ")
        
        tokens = tokenizer(expression)
        
        # 전체 수식 파싱 및 계산
        result, _ = parse_expression(tokens)
        print(f"Result: {result}")

    except (ValueError, ZeroDivisionError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()