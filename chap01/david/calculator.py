import re
operators = '+-*/'
def inputNum():
    try: 
        num = float(input("Enter number: "))
        return int(num)
    except:
        print('Invalid number input.')
        exit()
def inputOperator()->int:
    buffer = input("Enter Operator(+, -, *, /): ")
    for idx in range(4):
        if buffer[0] == operators[idx]:
            return idx
    print("Invalid operator." )
    exit()
def inputNumEnh():

        expression =  input("Enter expression: ")
        splitExpression = re.split(r'[\+\-\*/]',expression)
        if len(splitExpression) != 2:
            print("Invalid expression format. Please use 'number operator number'.")
            exit()
        
        try:
            left = int(left.strip())
        except ValueError:
            print('Invalid number input.')
            exit()
        try:    
            right = int(right.strip())
        except ValueError:
            print('Invalid number input.')
            exit()
        operator = re.search(r'[\+\-\*/]', expression).group(0)
        if not operator:
            print("Invalid operator.")
            exit()
        for idx in range(4):
            if operator == operators[idx]:
                operator = idx
                break

        return left, right, operator
    
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
opFunc = [add, subtract, multiply, divide]

# num1 = inputNum()
# num2 = inputNum()
# operator = inputOperator()
num1, num2, operator= inputNumEnh()
result = opFunc[operator](num1, num2)
print(f"Result: <{num1} {operators[operator]} {num2} = {result}>")



