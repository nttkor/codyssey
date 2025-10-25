# 1. LinkedList, CirculaList
#    0. class Node(self,data):  (문제에는 없지만 구현해야함)
#       1. self.data = data 
#       2. self.next = None 구현해야함
#    1. LinkedList 구현사항
#       1. 문제에는 없지만 def __init__(self): self.head = None구현해야함
#       2. insert(self,index,value) : 0<= index < last 범위 벗어나는 index, raise IndexError 처리
#          1. self.head에 데이터가 없는 경우 있는 경우, index가 범위를 벗어나는 경우를 구분해서 return값및 에러 처리해야함
#       3. delete(self,index) : index 범위 벗어 날경우 raise IndexError
#       4. to_list(self) : 
#       5. __len__(self)->int : 노드수 반환
#       6. 문제에는 없지만 디버깅을 위해 disply를 만들자
#    2. CircularList 구현 사항, last를 cursor라고 표현
#       1. 문제에는 없지만 def __init__(self): self.last = None 구현으로 시작
#       2. insert(self,value)
#          1. 추가시 self.last가 비었는지, 있는지 마지막인지를 잘 구분해서 처리해야함
#       3. delete(self,value)
#          1. 지울때도 없을때, 하나 있을때, 없을때 등등 상황 처리를 잘해야함
#       4. get_next(self) : 이건 last포인트를 last.next(즉 맨 처음)으로 바꾸고 출력하는것
#          1. self.last = self.last.next, return self.last.data(이전의 head data)
#       5. search(value) 아까 delete와 비슷 찾아지면 data return 하면 됨
#       6. 문제에는 없지만 디버깅을 위해 disply를 만들자
#       7. 구현후 모든 경우의 수 체크해보자

class Node:
    """단일 연결 리스트의 노드 클래스"""
    def __init__(self, data):
        self.data = data
        self.next = None
class LinkedList:
    """단일 연결 리스트 클래스"""
    def __init__(self):
        self.head = None

    def insert(self, index, value):
        """특정 인덱스에 노드 삽입"""
        if index < 0 or index > len(self):
            raise IndexError("인덱스가 범위를 벗어났습니다.")

        new_node = Node(value)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def delete(self, index):
        """특정 인덱스의 노드 삭제"""
        if index < 0 or index >= len(self):
            raise IndexError("인덱스가 범위를 벗어났습니다.")
        
        if index == 0:
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            current.next = current.next.next

    def to_list(self):
        """리스트의 모든 데이터를 리스트로 변환하여 반환"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def __len__(self):
        """리스트의 노드 수를 반환"""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def display(self):
        """리스트의 내용을 출력"""
        print("LinkedList:", " -> ".join(map(str, self.to_list())))

# LinkedList 테스트
print("--- LinkedList 테스트 ---")
ll = LinkedList()
ll.insert(0,30)
# 삽입 테스트
print("초기 상태:")
ll.display()
ll.insert(0, 10)
ll.insert(1, 30)
ll.insert(1, 20)
ll.display()
print("리스트 길이:", len(ll))
print("리스트 변환:", ll.to_list())

# 삭제 테스트
ll.delete(1)
ll.display()
print("리스트 길이:", len(ll))

# 예외 처리 테스트
try:
    ll.insert(5, 100)
except IndexError as e:
    print(e)
try:
    ll.delete(5)
except IndexError as e:
    print(e)
class CircularList:
    """원형 연결 리스트 클래스"""
    def __init__(self):
        self.last = None

    def insert(self, value):
        """리스트의 끝에 노드 삽입"""
        new_node = Node(value)
        if self.last is None:
            self.last = new_node
            new_node.next = new_node
        else:
            new_node.next = self.last.next
            self.last.next = new_node
            self.last = new_node

    def delete(self, value):
        """특정 값을 가진 노드 삭제"""
        if self.last is None:
            return

        # 리스트에 노드가 하나만 있는 경우
        if self.last.data == value and self.last.next == self.last:
            self.last = None
            return

        current = self.last.next
        prev = self.last

        # 노드를 순회하며 삭제할 값 찾기
        while True:
            if current.data == value:
                # 마지막 노드를 삭제하는 경우
                if current == self.last:
                    prev.next = self.last.next
                    self.last = prev
                else:
                    prev.next = current.next
                return
            
            # 다음 노드로 이동
            prev = current
            current = current.next
            if current == self.last.next:
                break

    def get_next(self):
        """last 포인터를 다음 노드로 이동하고 그 데이터를 반환"""
        if self.last is None:
            return None
        self.last = self.last.next
        return self.last.data

    def search(self, value):
        """값으로 노드 검색"""
        if self.last is None:
            return None

        current = self.last.next
        while True:
            if current.data == value:
                return current.data
            current = current.next
            if current == self.last.next:
                break
        return None

    def display(self):
        """리스트의 내용을 출력"""
        if self.last is None:
            print("CircularList: 비어있음")
            return
        
        nodes = []
        current = self.last.next
        while True:
            nodes.append(str(current.data))
            current = current.next
            if current == self.last.next:
                break
        print("CircularList:", " -> ".join(nodes), "(last: {})".format(self.last.data))

# CircularList 테스트
print("\n--- CircularList 테스트 ---")
cl = CircularList()

# 삽입 테스트
print("초기 상태:")
cl.display()
cl.insert(10)
cl.insert(20)
cl.insert(30)
cl.display()

# get_next 테스트
print("다음 노드 가져오기 (last 이동):", cl.get_next())
cl.display()

# 검색 테스트
print("값 20 검색:", cl.search(20))
print("값 99 검색:", cl.search(99))

# 삭제 테스트
cl.delete(20)
cl.display()
cl.delete(10)
cl.display()
cl.delete(30)
cl.display()
cl.delete(99) # 없는 값 삭제 테스트
cl.display()
