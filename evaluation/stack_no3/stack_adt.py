# stack_adt.py by Lee Jin Gul

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.capacity = 10   # 최대 10개
        self.count = 0       # 현재 스택 크기
        self.head = None     # 첫 노드
        self.upper = None    # 마지막(맨 위) 노드

    def push(self, value: any) -> bool:
        if self.count >= self.capacity:
            print("Stack is full.")
            return False

        new_node = Node(value)

        if self.count == 0:
            # 스택이 비어있으면 head와 upper 모두 새 노드
            self.head = new_node
            self.upper = new_node
        else:
            # 기존 upper.next에 연결 후 upper 갱신
            self.upper.next = new_node
            self.upper = new_node

        self.count += 1
        return True

    def pop(self) -> object | None:
        if self.count == 0:
            print("Stack is empty.")
            return None

        value = self.upper.value

        if self.count == 1:
            # 노드 1개일 때
            self.head = None
            self.upper = None
        else:
            # 마지막 전 노드 찾기
            prev = self.head
            for _ in range(self.count - 2):
                prev = prev.next
            self.upper = prev
            self.upper.next = None

        self.count -= 1
        return value

    def empty(self) -> bool:
        return self.count == 0

    def peek(self) -> object | None:
        if self.count == 0:
            print("Stack is empty. ")
            return None
        return self.upper.value
    
def main():
    # pass
    s = Stack()
    # print("Empty?", s.empty())  # True

    # for i in range(12):          # 10개 초과 push 테스트
    #     s.push(i)

    # print("Peek:", s.peek())     # 9

    # while not s.empty():
    #     print("Pop:", s.pop())

    # s.pop()                      # Stack is empty.


# 선택 사항: 테스트용 main
if __name__ == "__main__":
    main()