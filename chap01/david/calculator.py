def inputNum():
    try: 
        num = float(input("Enter number: "))
        return int(num)
    except:
        print('Invalid number input.')
        exit()
def inputOperator()->int:
    buffer = input("Enter Operator(+, -, *, /): ")
    operators = '+-*/'
    for idx in range(4):
        if buffer[0] == operators[idx]:
            return idx
    print("Invalid operator." )
    exit()

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
num1 = inputNum()
num2 = inputNum()
operator = inputOperator()
result = opFunc[operator](num1, num2)
print(f"Result: <{result}>")



