class Stack:
    def __init__(self):
        self.data = list()
    def __len__(self):
        return len(self)  #len(self.data)로 수정해야함,         return count로 하던지

    def push(self, value):
        if len(self.data) >= 10:
            print("Stack is Full.")
            return False
        else:
            self.data.append(value)
            return True
    def pop(self):
        if self.empty():
            print("Stack is Empty.")
            return None  # 평가에서는 False로 한것 같음
        else:
            return self.data.pop()
    def empty(self):
        if len(self.data) == 0:
            return True
        else:
            return False
    def peek(self):
        if self.empty():
            print("Empty")
            return None #평가에서는 False로 한것 같음
        else:
            return self.data[-1]
st = Stack()
print('pop',st.pop())
print('peek',st.peek())
for i in range(11):
    print('push',i,st.push(i), st.data)
print('peek',st.peek())
for i in range(11):
    print('pop',i,st.pop(), st.data)
print(st.data)

    
        
    
