import re

def tokenizer(expression):
    """수학 표현식 문자열을 토큰으로 분할합니다. 괄호는 처리하지 않습니다."""
    # 숫자 (음수 포함), 연산자를 찾기 위해 정규식을 사용합니다.
    # 빼기 연산자와 음수를 구분하기 위해 정규식을 수정합니다.
    tokens = re.findall(r'(\d+\.?\d*)|([-+*/])', expression)
    # re.findall은 그룹을 튜플로 반환하므로, 튜플을 평탄화하고 빈 문자열을 제거합니다.
    tokens = [item for sublist in tokens for item in sublist if item]

    # `(-5)`와 같이 음수 부호가 음수의 일부인 경우를 처리하기 위한 추가 로직입니다.
    # 괄호 처리가 없으므로 이 로직은 더 간단해집니다.
    refined_tokens = []
    for i, token in enumerate(tokens):
        if token == '-' and (i == 0 or tokens[i-1] in '+-*/'):
            # '-'가 시작 부분이나 연산자 뒤에 오고 숫자 뒤에 오는 경우,
            # 음수의 일부입니다. 다음 토큰과 병합합니다.
            if i + 1 < len(tokens) and re.match(r'\d', tokens[i+1]):
                refined_tokens.append(token + tokens[i+1])
                tokens[i+1] = '' # 다음 토큰을 건너뛰도록 표시
            else:
                refined_tokens.append(token)
        elif token != '': # 비어 있지 않은 토큰 추가
            refined_tokens.append(token)

    return refined_tokens


def infix_to_postfix(tokens):
    """중위 표기법 토큰 목록을 후위 표기법 토큰 목록으로 변환합니다. 괄호는 처리하지 않습니다."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operator_stack = []

    for token in tokens:
        if re.match(r'-?\d+\.?\d*', token):
            output.append(token)
        elif token in precedence:
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
        if re.match(r'-?\d+\.?\d*', token):
            operand_stack.append(float(token))
        elif token in '+-*/':
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

calculate_expression('1+2*3- 5')