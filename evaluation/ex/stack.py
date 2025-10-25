class Stack:
    def __init__(self):
        self.data = list()
    def push(self, value):
        if len(self.data) >= 10:
            print("Full")
            return False
        else:
            self.data.append(value)
            return True
    def pop(self):
        if self.empty():
            print("Empty")
            return None
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
            return None
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

    
        
    
