import re
operators = '+-*/'

# 입력을 받아 숫자2개 연산자로 분리함
def inputNumEnh():
    expression = input("Enter expression: ").replace(" ", "")  # 공백 제거

    # 정규표현식으로 수식에서 두 숫자와 연산자 추출
    #^(-?\d+\.?\d*)(([\+\-\*/])(-?\d+\.?\d*))*$
    match = re.match(r'^(-?\d+\.?\d*)([\+\-\*/])(-?\d+\.?\d*)$', expression)
    if not match:
        print("Invalid expression format. Please use 'number operator number'.")
        exit()

    left, operator, right = match.groups()

    try:
        left = int(float(left))
        right = int(float(right))
    except ValueError:
        print("Invalid number input.")
        exit()

    operator_idx = operators.index(operator)
    return left, right, operator_idx

# 연산함수  
def add(a, b):
    return a+b
def subtract(a, b):
    return a-b
def multiply(a, b):
    return a*b
def divide(a, b):
    if(b != 0):
        return a/b
    else:
        print("Error: Division by zero." )
        exit()
#연산함수 주소 배열
opFunc = [add, subtract, multiply, divide]
if __name__ == "__main__":

    # 계산식을 입력 받아 숫자2개 연산자로 분리함
    num1, num2, operator= inputNumEnh()
    # 연산을함 연산자에 해당하는 함수를 배열로 처리
    result = opFunc[operator](num1, num2)
    #결과 출력
    print(f"Result: <{num1} {operators[operator]} {num2} = {result}>")
else:
    print("Plase execute at main")


