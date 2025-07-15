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

# 입력을 받아 숫자2개 연산자로 분리함
def inputNumEnh():

        expression =  input("Enter expression: ")
        splitExpression = re.split(r'[\+\-\*/]',expression)
        if len(splitExpression) != 2:
            print("Invalid expression format. Please use 'number operator number'.")
            exit()
        
        try:
            left = int(float(left.strip()))
        except ValueError:
            print('Invalid number input.')
            exit()
        try:    
            right = int(float(right.strip()))
        except ValueError:
            print('Invalid number input.')
            exit()
        #연산자를 찾아 
        operator = re.search(r'[\+\-\*/]', expression).group(0)
        #연산자가 없으면 에러처리
        if not operator:
            print("Invalid operator.")
            exit()
        #연산자에 해당하는 인덱스를 operatord에 저장
        for idx in range(4):
            if operator == operators[idx]:
                operator = idx
                break
        return left, right, operator

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

# num1 = inputNum()
# num2 = inputNum()
# operator = inputOperator()
# 계산식을 입력 받아 숫자2개 연산자로 분리함
num1, num2, operator= inputNumEnh()
# 연산을함 연산자에 해당하는 함수를 배열로 처리
result = opFunc[operator](num1, num2)
#결과 출력
print(f"Result: <{num1} {operators[operator]} {num2} = {result}>")



