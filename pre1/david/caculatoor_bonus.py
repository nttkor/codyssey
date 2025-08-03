def inputNumEnh():
    expression = input("Enter expression: ").replace(" ", "")  # 공백 제거

    operators = ['+', '-', '*', '/'] 
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    found_operator = ''
    operator_index = -1

    # 가장 왼쪽부터 유효한 연산자를 찾습니다.
    # 이때, 음수 부호('-')와의 충돌을 해결하는 것이 핵심입니다.
    # '2 * -2' 와 같은 경우를 처리하기 위해, 연산자 뒤에 오는 '-'는 다음 숫자의 부호로 간주합니다.
    
    # 팁: 연산자 우선순위를 역순으로 찾아 가장 큰 범위의 연산자를 찾는 방법도 있지만,
    # 여기서는 'A op B' 형태에서 가장 먼저 나오는 '유효한' 연산자를 찾습니다.
    # 즉, 뺄셈(-) 연산자가 첫 번째 피연산자의 음수 부호와 겹치지 않도록 주의합니다.
    checkexpression = expression
    minus = False
    if len(expression) == 0:
        print("Invalid expression format. Please use 'number operator number'.")
        exit()
    if expression[0] == '-':
        checkexpression = expression[1:]
        minus = True
    if len(checkexpression) == 0:
        print("Invalid expression format. Please use 'number operator number'.")
        exit()
    for i, char in enumerate(checkexpression):
        if char in numbers:
            continue
        if char in operators:
            if i==0:
                print("Invalid expression format. Please use 'number operator number'.")
                exit()
            if len(checkexpression) > i+1 and not checkexpression[i+1] in '+*/' and checkexpression[i+1] in '0123456789':
                found_operator = char
                operator_index = i
                break
            else:
                break 
        else:
            break

    if operator_index == -1:
        print("Invalid operator.")
        exit() 
    # 연산자 앞뒤로 숫자를 분리합니다.
    left = checkexpression[:operator_index] 
    if minus:
        left = '-' + left  # 음수 부호를 복원합니다.
    right = checkexpression[operator_index + 1:]
    if not left or not right:
        print("Invalid expression format. Please use 'number operator number'.")
        exit() 
    # 숫자 변환 시도
    try:
        left = int(float(left))
        right = int(float(right))   
    except ValueError:
        print("Invalid number input.")
        exit()  

    # 연산자 인덱스 찾기
    operator_idx = operators.index(found_operator)
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
        return int(a/b)
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
    operatorstr = '+-*/'  # 연산자 목록을 다시 정의
    print(f"Result: <{num1} {operatorstr[operator]} {num2} = {result}>")
else:
    print("Plase execute at main")


