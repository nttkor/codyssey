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

# ------------------ 단순 연결 리스트 linkedlist ------------------
# -*- coding: utf-8 -*-
# linkedlist / circularlist - automatic grading friendly implementation
# All indentation uses 4 spaces.

# ------------------ 단순 연결 리스트 linkedlist ------------------
# ------------------ 단순 연결 리스트 linkedlist ------------------
class _Node:
    __slots__ = ('value', 'next')

    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt


class LinkedList:
    def __init__(self):
        self._head = None
        self._size = 0

    def insert(self, index, value):
        if not isinstance(index, int):
            raise TypeError
        if index < 0 or index > self._size:
            raise IndexError

        new_node = _Node(value)

        if index == 0:                 # 맨 앞에 삽입
            new_node.next = self._head
            self._head = new_node
        else:
            prev = self._head
            for _ in range(index - 1):
                prev = prev.next
            new_node.next = prev.next
            prev.next = new_node

        self._size += 1

    def delete(self, index):
        if not isinstance(index, int):
            raise TypeError
        if index < 0 or index >= self._size:
            raise IndexError

        if index == 0:
            deleted = self._head
            self._head = self._head.next
        else:
            prev = self._head
            for _ in range(index - 1):
                prev = prev.next
            deleted = prev.next
            prev.next = deleted.next

        self._size -= 1
        return deleted.value

    def to_list(self):
        result = []
        cur = self._head
        while cur:
            result.append(cur.value)
            cur = cur.next
        return result

    def __len__(self):
        return self._size


# ------------------ 원형 연결 리스트 circularlist ------------------

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self._cursor = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    # 문제 조건:
    # - 첫 노드 → 자기 자신을 가리키는 원형
    # - N개일 때 → cursor 뒤 삽입, cursor = 새 노드
    def insert(self, value):
        new_node = Node(value)

        if self._cursor is None:                 # 0개
            new_node.next = new_node
            self._cursor = new_node
        else:                                     # N개
            new_node.next = self._cursor.next
            self._cursor.next = new_node
            self._cursor = new_node              # 문제 의도: cursor를 새 노드로 이동

        self._size += 1

    # cursor = cursor.next, return cursor.value
    def get_next(self):
        if self._cursor is None:
            return None
        self._cursor = self._cursor.next
        return self._cursor.value

    # value 존재 여부
    def search(self, value):
        if self._cursor is None:
            return False

        cur = self._cursor
        for _ in range(self._size):
            if cur.value == value:
                return True
            cur = cur.next
        return False

    # 문제 조건:
    # - value 매칭 첫 노드 삭제
    # - cursor 삭제 → cursor = prev
    # - size=1 → cursor=None
    def delete(self, value):
        if self._cursor is None:
            return False

        prev = self._cursor
        cur = self._cursor

        for _ in range(self._size):
            if cur.value == value:

                # 노드 1개
                if self._size == 1:
                    self._cursor = None
                else:
                    prev.next = cur.next
                    if cur is self._cursor:
                        self._cursor = prev

                self._size -= 1
                return True

            prev = cur
            cur = cur.next

        return False

    # 디버깅용 (자동채점은 사용 안함)
    def show(self):
        if self._cursor is None:
            return []

        result = []
        cur = self._cursor
        for _ in range(self._size):
            result.append(cur.value)
            cur = cur.next
        return result
lst = CircularLinkedList()
lst.insert(10)
lst.insert(20)
lst.insert(30)

print(lst.show())        # [30, 10, 20]
print(lst.get_next())    # 10
print(lst.get_next())    # 20

lst.delete(20)
print(lst.show())        # [30, 10]

lst.delete(10)
print(lst.show())        # [30]

lst.delete(30)
print(lst.show())        # []
