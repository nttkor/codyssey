def inputNumEnh():
    expression = input("Enter expression: ").replace(" ", "")  # 공백 제거

    operators = ['+', '-', '*', '/'] 
    
    found_operator = ''
    operator_index = -1

    # 가장 왼쪽부터 유효한 연산자를 찾습니다.
    # 이때, 음수 부호('-')와의 충돌을 해결하는 것이 핵심입니다.
    # '2 * -2' 와 같은 경우를 처리하기 위해, 연산자 뒤에 오는 '-'는 다음 숫자의 부호로 간주합니다.
    
    # 팁: 연산자 우선순위를 역순으로 찾아 가장 큰 범위의 연산자를 찾는 방법도 있지만,
    # 여기서는 'A op B' 형태에서 가장 먼저 나오는 '유효한' 연산자를 찾습니다.
    # 즉, 뺄셈(-) 연산자가 첫 번째 피연산자의 음수 부호와 겹치지 않도록 주의합니다.
    
    for i, char in enumerate(expression):
        # 첫 번째 문자가 '-'이고 연산자가 아님을 보장합니다.
        # 즉, '-5+3'에서 첫 번째 '-'는 5의 부호입니다.
        if i == 0 and char == '-':
            continue # 첫 번째 문자가 '-'이면 건너뛰고 다음 문자부터 탐색

        if char in operators:
            # 연산자 뒤에 아무것도 없으면 오류
            if i == len(expression) - 1:
                print("Invalid expression format. Please use 'number operator number'.")
                exit()
            
            # '2 * -2'처럼 연산자 뒤에 '-'가 오는 경우를 처리
            # char는 연산자, expression[i+1]은 다음 문자
            if expression[i+1] == '-':
                # 만약 그 다음 문자가 숫자가 아니면 (예: '5*-', '5*--'), 이는 유효하지 않음
                if i + 2 >= len(expression) or not expression[i+2].isdigit():
                    print("Invalid expression format. Number expected after operator and sign.")
                    exit()
                # 유효한 형태라면 (예: '*-5'), 이 연산자 위치를 사용합니다.
                found_operator = char
                operator_index = i
                break # 유효한 연산자 찾았으니 종료
            
            # '1++2'처럼 연산자 뒤에 또 다른 연산자가 오는 경우 (단, 다음이 '-'가 아닌 경우)
            elif expression[i+1] in operators:
                print("Invalid expression format. Multiple operators in sequence.")
                exit()
            
            # 위 예외들에 해당하지 않는 일반적인 유효한 연산자를 찾은 경우
            else:
                found_operator = char
                operator_index = i
                break # 유효한 연산자 찾았으니 종료

    # 연산자를 찾지 못했다면 오류
    if operator_index == -1:
        print("Invalid expression format. No valid operator found.")
        exit()

    left_str = expression[:operator_index]
    right_str = expression[operator_index + 1:]

    # float() 변환을 시도하고 실패하면 오류 처리
    try:
        left = int(float(left_str))
        right = int(float(right_str))
    except ValueError:
        # float() 변환 실패는 숫자가 아니거나 형식이 잘못된 경우
        print("Invalid number format in expression.")
        exit()
    
    # left_str 이나 right_str 이 빈 문자열인 경우 float() 변환에서 ValueError 발생
    # 예를 들어, "+5", "-5" 같은 입력은 left_str이 빈 문자열이 될 수 있음.
    # float('')는 ValueError 발생시키므로, try-except로 처리됩니다.
    # 하지만 첫 번째 피연산자가 빈 문자열인 경우를 명시적으로 막는 것이 더 명확합니다.
    if not left_str or not right_str:
        print("Invalid expression format. Operands cannot be empty.")
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
    operatorstr = '+-*/'  # 연산자 목록을 다시 정의
    print(f"Result: <{num1} {operatorstr[operator]} {num2} = {result}>")
else:
    print("Plase execute at main")


