class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.top = None
        self.count = 0


    def push(self, value:any) ->bool:
        if self.count == 10:
            print("Stack is full.")
            return False
        new_node = Node(value)
        if self.top == None:
            print("1st item push")
            self.top = new_node
        else:
            new_node.next = self.top
            print("2nd+ item push")
            self.top = new_node
        self.count += 1
        return True
    
    def pop(self) ->object|None:
        if self.top == None:
            print("Stack is empty.")
            return None
        else:
            value = self.top.value
            self.top = self.top.next
            self.count -= 1 #빼먹으면 안 된다!
            return value
        
    def empty(self) -> bool:
        return self.count == 0
    
    def peek(self) -> object|None:
        if self.top == None:
            print("Stack is empty.")
            return None
        else:
            return self.top.value
        
    #커스텀 메소드 (테스트용)
    def tolist(self):
        result = []
        node = self.top
        for i in range(self.count -1): #여기서 출력 에러가 많이 났는데,  -> 수정: range(self.count)로 하기
                                        #self.count -=, += 을 제대로 반영 못한 결과였다. 
                                        # While node: 였으면 편하게 갔겠지만, 
                                        # 그려면 counter = 0, counter+=을 만들어줘야 했겠지

            result.append(node.value)
            node = node.next
        print(f"stack: {result}")
        print(f"stack length: {self.count}")
        return result
    

def main():
    print("TEST HERE")
    



if __name__ == "__main__":
    main()