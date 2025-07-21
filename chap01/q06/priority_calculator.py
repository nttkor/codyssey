def suf_change(n) :
    stack = []
    result = ''
    for i in n:
        if i == '+' or i == '-': #우선순위 1 / 1
            while stack and stack[-1] != '(':
                result += stack.pop()
            stack.append(i)
        elif i == '*' or i == '/': #우선순위 2 / 2
            while stack and (stack[-1] == '*' or stack[-1] == '/'):
                result += stack.pop()
            stack.append(i)
        elif i == '(': #우선순위 0 / 3
            stack.append(i)
        elif i == ')': #(를 만날때까지 모두 pop
            while stack and stack[-1] != '(':
                result += stack.pop()
            stack.pop()
        else:
            result += i

    while stack:
        result += stack.pop()
    return result
def Calculation(x):
    stack = []
    for i in x:
        if i == '+':
            stack.append(stack.pop()+stack.pop())
        elif i == '-': 
            stack.append(-(stack.pop()-stack.pop()))
        elif i == '*': 
            stack.append(stack.pop()*stack.pop())
        elif i == '/': 
            divide = stack.pop()
            stack.append(stack.pop()/divide)
        else:
            stack.append(int(i))
    return stack.pop()
postfix = input("Enter postfix expression: ")
postfix = suf_change(postfix)
print(f"Postfix expression: {postfix}")
result = Calculation(postfix)
print(f"Result: {result}")

