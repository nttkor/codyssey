# import re  # re 모듈을 더 이상 사용하지 않습니다.

def tokenizer(expression):
    """수학 표현식 문자열을 토큰으로 분할합니다. 괄호는 처리하지 않습니다."""
    tokens = []
    current_token = ""
    expression = expression.replace(" ", "") # 공백 제거

    i = 0
    while i < len(expression):
        char = expression[i]

        if char.isdigit() or (char == '.' and current_token) or (char == '-' and not current_token and (i == 0 or expression[i-1] in '+-*/')):
            # 숫자, 소수점 (앞에 숫자가 있는 경우), 또는 음수 부호 (시작 또는 연산자 뒤)
            current_token += char
        else:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            if char in '+-*/':
                tokens.append(char)
            # 괄호 처리는 이 버전에서 고려하지 않습니다.
        i += 1

    if current_token:
        tokens.append(current_token)

    return tokens


def infix_to_postfix(tokens):
    """중위 표기법 토큰 목록을 후위 표기법 토큰 목록으로 변환합니다. 괄호는 처리하지 않습니다."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operator_stack = []

    for token in tokens:
        # 숫자인지 확인 (음수 포함)
        try:
            float(token)
            output.append(token)
        except ValueError:
            if token in precedence:
                while (operator_stack and operator_stack[-1] in precedence and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            # 괄호 관련 로직 제거

    while operator_stack:
        output.append(operator_stack.pop())

    return output

def evaluate_postfix(postfix_tokens):
    """후위 표기법 토큰 목록을 평가합니다."""
    operand_stack = []

    for token in postfix_tokens:
        # 숫자인지 확인 (음수 포함)
        try:
            operand_stack.append(float(token))
        except ValueError:
            if token in '+-*/':
                if len(operand_stack) < 2:
                    raise ValueError("잘못된 후위 표현식: 피연산자가 부족합니다.")
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                if token == '+':
                    operand_stack.append(operand1 + operand2)
                elif token == '-':
                    operand_stack.append(operand1 - operand2)
                elif token == '*':
                    operand_stack.append(operand1 * operand2)
                elif token == '/':
                    if operand2 == 0:
                        raise ValueError("0으로 나눌 수 없습니다.")
                    operand_stack.append(operand1 / operand2)

    if len(operand_stack) != 1:
        raise ValueError("잘못된 후위 표현식: 피연산자가 너무 많습니다.")

    return operand_stack[0]

def calculate_expression(expression):
    """표현식을 토큰화하고 후위로 변환한 다음 평가합니다."""
    tokens = tokenizer(expression)
    postfix_tokens = infix_to_postfix(tokens)
    result = evaluate_postfix(postfix_tokens)
    return result
def main():
    print(calculate_expression('1+2*3- 5'))
    print(calculate_expression('10 + 2 * 6'))
    print(calculate_expression('100 * 2 + 12'))
    print(calculate_expression('100 * ( 2 + 12 )'))
    print(calculate_expression('100 * ( 2 + 12 ) / 14'))            


if __name__ == "__main__":
    main()