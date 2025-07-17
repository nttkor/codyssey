import re
operators = '+-*/'
#숫자를 입력받는 함수
def inputNum():
    try: 
        num = float(input("Enter number: "))
        return int(num)
    except:
        print('Invalid number input.')
        exit()
# 오퍼레이터를 입력받는 함수
def inputOperator()->int:
    buffer = input("Enter Operator(+, -, *, /): ")
    for idx in range(4):
        if buffer[0] == operators[idx]:
            return idx
    print("Invalid operator." )
    exit()

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
    num1 = inputNum()
    num2 = inputNum()
    operator = inputOperator()

    # 연산을함 연산자에 해당하는 함수를 배열로 처리
    result = opFunc[operator](num1, num2)
    #결과 출력
    print(f"Result: <{num1} {operators[operator]} {num2} = {result}>")
else:
    print("Plase execute at main")


