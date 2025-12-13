# 아래의 클래스 2개 작성 (자동채점은 지정 class와 method시그니처와 반환 규약을 따라야 한다.)
# 1. Python 코드로 단순 연결 리스트 구조를 완성한다.
# 단순 연결 리스트의 이름은 linkedlist로 만든다.
# 단순 연결 리스트에 새로운 항목을 임의 위치에 추가 할 수 있도록 추가 함수를 insert() 로 추가한다.
# 단순 연결 리스트의 특정 항목을 삭제 할 수 있도록 삭제 함수를 delete()로 추가한다. -> 삭제완료시 삭제된 데이터 값을 리턴한다.
# 값은 숫자나 영어문자열 등의 값을 받아 저장할 수 있도록 만든다.
# 추가 함수의 경우 첫번째 항목으로도 추가 할 수 있어야 하고 마지막 항목으로도 추가가 가능해야 한다.
# 처음부터 끝까지 순차적으로 가져오는 to_list() 함수를 추가한다.
# 전체 데이타의 항목의 갯수를 가져오는 __len__(self) 함수를 추가한다.
# Error 종류는 IndexError 케이스를 에러 처리를 적절히 해줘야하고, 그 외엔 Exception 으로 처리 하거나 해당 관련 Error 처리를 하도록 한다.(단, 출제 문제에는 IndexError만 언급됨)
#    1. LinkedList 구현사항
#       1. 문제에는 없지만 def __init__(self): self.head = None구현해야함
#       2. insert(self,index,value) : 0<= index < last 범위 벗어나는 index, raise IndexError 처리
#          1. self.head에 데이터가 없는 경우 있는 경우, index가 범위를 벗어나는 경우를 구분해서 return값및 에러 처리해야함
#       3. delete(self,index) : index 범위 벗어 날경우 raise IndexError
#       4. to_list(self) : 모든데이터를 리스트로 묶어서 리턴
#       5. __len__(self)->int : 노드수 반환
#       6. 문제에는 없지만 디버깅을 위해 disply를 만들자


# 2. Python 코드로 원형 연결 리스트(Circular Linked List)를 구현한다 - 커서 기반 원형 연결 리스트/단일 구조 리스트
# 이때 원형 연결 리스트의 이름은 circularlist로 만든다.
# 원형 연결 리스트에 임의의 위치에 새로운 원소를 추가 할 수 있도록 추가 함수를 insert()로 만든다.
# - delete(value) -> bool: 값이 같은 첫 노드 삭제(성공시 True, 실패시 False). 삭제 노드가 커서면 이전 노드로 이동한다. 만약 노드가 1개 있고 삭제되면 빈 상태가 된다.
# 원형 연결 리스트에서 다음 항목으로 넘어 가서 항목을 가져오는 get_next() 함수를 추가한다.
# - insert(value) -> None: 기존 노드가 0 개 일 경우, 단일 노드 원형을 구성하여 리턴 / 기존 노드 n개 일 경우, 커서 뒤 삽입 후 커서를 새 노드로 이동
# - get_next() -> Object | None: 기존 노드가 0개 일 경우, None 리턴 / n개 일 경우, 커서 다음 노드 이동후 그 값을 반환(리스트 순환)
# 데이타/값을 입력해서 검색하는 search() 함수를 추가하고 구현
# - search(value) -> bool: 해당 value의 데이타 존재 여부(True/False)를 반환
# 원형 연결 리스트에서 특정 원소를 삭제하는 delete() 함수를 만든다
# Error 종류는 IndexError 케이스를 에러 처리를 적절히 해줘야하고, 그 외엔 Exception 으로 처리 하거나 해당 관련 Error 처리를 하도록 한다.(원형 연결 리스트에서는 Exception 처리 언급없음)
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
    def __init__(self, value):
        self.value = value
        self.next : Node | None= None
class linkedlist:
    def __init__(self):
        self.head : Node | None= None
        self.size = 0
    def insert(self, index: int, value) -> None:
        if not isinstance(index,int):
            raise TypeError
        if index < 0 or index > self.size:
            raise IndexError
        new_node = Node(value)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            prev = self.head
            for _ in range(index - 1):
                if prev is None:
                    raise IndexError
                prev = prev.next
            new_node.next = prev.next
            prev.next = new_node
        self.size += 1
    def delete(self, index: int):
        if not isinstance(index,int):
            raise TypeError
        if index < 0 or index >= self.size:
            raise IndexError
        if index == 0:
            if self.head is None:
                raise IndexError
            deleted_value = self.head.value
            self.head = self.head.next
        else:
            prev = self.head
            for _ in range(index - 1):
                # if prev is None:
                #     raise IndexError
                prev = prev.next
            # if prev.next is None:
            #     raise IndexError
            deleted_value = prev.next.value
            prev.next = prev.next.next
        self.size -= 1
        return deleted_value
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result
    def __len__(self) -> int:
        return self.size
    
    def display(self,msg=""):
        print(msg,end='>> ')
        result = []
        if self.size == 0:
            print("Empty")
        else:
            current = self.head
            while current:
                result.append(str(current.value))
                current = current.next
            print("->".join(result))
    def __delitem__(self,index:int):
        self.delete(index)

# ll = linkedlist()
# for i in range(5):
#     ll.insert(i,i+1)
#     ll.display(f'After inserting {i+1} at index {i}')
# ll.display('Current List:')
# for _ in range(5):
#     deleted_value = ll.delete(0)
#     ll.display(f'After deleting value {deleted_value} from index 0')
    
class LinkedList(list):
    def insert(self, index: int, value: int) -> None:
        if index < 0 or index > len(self):
            raise IndexError
        super().insert(index, value)
    def delete(self, index: int):
        if index < 0 or index >= len(self):
            raise IndexError
        return self.pop(index)
    def display(self,msg=""):
        print(msg,end='>> ')
        if len(self) == 0:
            print("Empty")
        else:
            print("->".join(str(x) for x in self))

ll2 = LinkedList()
for i in range(5):
    ll2.insert(i,i+1)
    ll2.display(f'After inserting {i+1} at index {i}')
        
for i in range(5):
    deleted_value = ll2.delete(0)
    ll2.display(f'After deleting value {deleted_value} from index 0')
        