# linked_list.py

class Node:
    """연결 리스트의 노드 클래스"""
    def __init__(self, data):
        self.data = data
        self.next = None  # 다음 노드를 가리키는 포인터


class LinkedList:
    """단순 연결 리스트 클래스"""
    def __init__(self):
        self.head = None  # 리스트의 시작 노드

    def append(self, data):
        """리스트 끝에 새 노드를 추가"""
        new_node = Node(data)
        if self.head is None:  # 리스트가 비어있으면
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def prepend(self, data):
        """리스트 시작에 새 노드를 추가"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, key):
        """값이 key인 노드를 삭제"""
        current = self.head

        # 헤드 노드가 삭제 대상일 경우
        if current and current.data == key:
            self.head = current.next
            current = None
            return

        prev = None
        while current and current.data != key:
            prev = current
            current = current.next

        if current is None:  # key가 존재하지 않음
            print(f"{key} not found in the list.")
            return

        # 노드 삭제
        prev.next = current.next
        current = None

    def find(self, key):
        """값이 key인 노드를 찾고 반환"""
        current = self.head
        while current:
            if current.data == key:
                return current
            current = current.next
        return None

    def print_list(self):
        """리스트를 출력"""
        current = self.head
        elements = []
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements))


# 테스트 예시
if __name__ == "__main__":
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.prepend(5)
    ll.print_list()  # 출력: 5 -> 10 -> 20

    ll.delete(10)
    ll.print_list()  # 출력: 5 -> 20

    node = ll.find(20)
    if node:
        print(f"Found: {node.data}")  # 출력: Found: 20
