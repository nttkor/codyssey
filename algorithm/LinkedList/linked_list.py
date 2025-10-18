class Node:
    """연결 리스트의 노드를 표현하는 클래스입니다."""
    def __init__(self, data):
        """
        노드를 초기화합니다.
        
        Args:
            data: 노드에 저장될 데이터입니다.
        """
        self.data = data
        self.next = None  # 다음 노드를 가리키는 포인터. 초기에는 None으로 설정합니다.
class LinkedList:
    """단일 연결 리스트를 구현한 클래스입니다."""
    def __init__(self):
        """
        연결 리스트를 초기화합니다.
        
        head는 리스트의 첫 번째 노드를 가리키며, 초기에는 None입니다.
        """
        self.head = None

    def is_empty(self):
        """
        리스트가 비어 있는지 확인합니다.
        
        Returns:
            bool: 리스트가 비어 있으면 True, 아니면 False를 반환합니다.
        """
        return self.head is None

    def append(self, data):
        """
        리스트의 끝에 새로운 노드를 추가합니다.
        
        Args:
            data: 새 노드에 저장할 데이터입니다.
        """
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            return
        
        current_node = self.head
        while current_node.next:
            current_node = current_node.next
        current_node.next = new_node

    def prepend(self, data):
        """
        리스트의 맨 앞에 새로운 노드를 추가합니다.
        
        Args:
            data: 새 노드에 저장할 데이터입니다.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data):
        """
        특정 데이터를 가진 노드를 리스트에서 삭제합니다.
        
        Args:
            data: 삭제할 노드의 데이터입니다.
        """
        if self.is_empty():
            return

        # 헤드 노드를 삭제하는 경우
        if self.head.data == data:
            self.head = self.head.next
            return

        current_node = self.head
        while current_node.next and current_node.next.data != data:
            current_node = current_node.next
        
        # 노드를 찾았을 경우
        if current_node.next:
            current_node.next = current_node.next.next

    def display(self):
        """
        리스트의 모든 노드를 순회하며 데이터를 출력합니다.
        """
        elements = []
        current_node = self.head
        while current_node:
            elements.append(current_node.data)
            current_node = current_node.next
        print(" -> ".join(map(str, elements)))

# 연결 리스트 사용 예제
if __name__ == '__main__':
    print("--- 단일 연결 리스트 ---")
    llist = LinkedList()
    llist.append(1)
    llist.append(2)
    llist.append(3)
    llist.display()  # 출력: 1 -> 2 -> 3

    llist.prepend(0)
    llist.display()  # 출력: 0 -> 1 -> 2 -> 3

    llist.delete(2)
    llist.display()  # 출력: 0 -> 1 -> 3
    
    llist.delete(0)
    llist.display() # 출력: 1 -> 3

# Node 클래스 (공통)
class Node:
    """연결 리스트의 노드를 표현하는 클래스입니다."""
    def __init__(self, data):
        """
        노드를 초기화합니다.
        
        Args:
            data: 노드에 저장될 데이터입니다.
        """
        self.data = data
        self.next = None  # 다음 노드를 가리키는 포인터. 초기에는 None으로 설정합니다.


class LinkedList:
    """단일 연결 리스트를 구현한 클래스입니다."""
    def __init__(self):
        """
        연결 리스트를 초기화합니다.
        
        head는 리스트의 첫 번째 노드를 가리키며, 초기에는 None입니다.
        """
        self.head = None

    def is_empty(self):
        """
        리스트가 비어 있는지 확인합니다.
        
        Returns:
            bool: 리스트가 비어 있으면 True, 아니면 False를 반환합니다.
        """
        return self.head is None

    def append(self, data):
        """
        리스트의 끝에 새로운 노드를 추가합니다.
        
        Args:
            data: 새 노드에 저장할 데이터입니다.
        """
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            return
        
        current_node = self.head
        while current_node.next:
            current_node = current_node.next
        current_node.next = new_node

    def prepend(self, data):
        """
        리스트의 맨 앞에 새로운 노드를 추가합니다.
        
        Args:
            data: 새 노드에 저장할 데이터입니다.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at(self, position, data):
        """
        특정 위치에 새로운 노드를 삽입합니다.
        
        Args:
            position (int): 노드를 삽입할 위치(0부터 시작).
            data: 새 노드에 저장할 데이터입니다.
        
        Raises:
            IndexError: 인덱스가 범위를 벗어날 경우 발생합니다.
        """
        if position < 0:
            raise IndexError("위치는 음수가 될 수 없습니다.")
        
        # 0번 위치에 삽입하는 경우 (prepend와 동일)
        if position == 0:
            self.prepend(data)
            return

        new_node = Node(data)
        current_node = self.head
        count = 0
        
        # 삽입할 위치의 바로 앞 노드까지 이동
        while current_node and count < position - 1:
            current_node = current_node.next
            count += 1

        # 위치가 리스트의 끝을 넘어선 경우
        if not current_node:
            raise IndexError("위치가 리스트의 범위를 벗어났습니다.")
        
        new_node.next = current_node.next
        current_node.next = new_node

    def delete(self, data):
        """
        특정 데이터를 가진 노드를 리스트에서 삭제합니다.
        
        Args:
            data: 삭제할 노드의 데이터입니다.
        """
        if self.is_empty():
            return

        # 헤드 노드를 삭제하는 경우
        if self.head.data == data:
            self.head = self.head.next
            return

        current_node = self.head
        while current_node.next and current_node.next.data != data:
            current_node = current_node.next
        
        # 노드를 찾았을 경우
        if current_node.next:
            current_node.next = current_node.next.next

    def display(self):
        """
        리스트의 모든 노드를 순회하며 데이터를 출력합니다.
        """
        elements = []
        current_node = self.head
        while current_node:
            elements.append(current_node.data)
            current_node = current_node.next
        print(" -> ".join(map(str, elements)) if elements else "리스트가 비어 있습니다.")




class CircularLinkedList:
    """순환 연결 리스트를 구현한 클래스입니다."""
    def __init__(self):
        """
        순환 연결 리스트를 초기화합니다.
        
        last는 리스트의 마지막 노드를 가리키며, 초기에는 None입니다.
        """
        self.last = None

    def is_empty(self):
        """
        리스트가 비어 있는지 확인합니다.
        
        Returns:
            bool: 리스트가 비어 있으면 True, 아니면 False를 반환합니다.
        """
        return self.last is None

    def append(self, data):
        """
        리스트의 끝(last 다음)에 새로운 노드를 추가합니다.
        
        Args:
            data: 새 노드에 저장할 데이터입니다.
        """
        new_node = Node(data)
        if self.is_empty():
            self.last = new_node
            new_node.next = new_node # 자신을 가리켜 순환 구조를 만듭니다.
        else:
            new_node.next = self.last.next # 새 노드의 next가 기존의 첫 노드를 가리킵니다.
            self.last.next = new_node      # 기존의 마지막 노드가 새 노드를 가리킵니다.
            self.last = new_node           # last 포인터를 새 노드로 업데이트합니다.

    def prepend(self, data):
        """
        리스트의 맨 앞(last.next)에 새로운 노드를 추가합니다.
        
        Args:
            data: 새 노드에 저장할 데이터입니다.
        """
        new_node = Node(data)
        if self.is_empty():
            self.last = new_node
            new_node.next = new_node
        else:
            new_node.next = self.last.next
            self.last.next = new_node
    
    def insert_at(self, index, data):
        """
        특정 인덱스에 새로운 노드를 삽입합니다.
        
        Args:
            index (int): 노드를 삽입할 위치의 인덱스입니다.
            data: 새 노드에 저장할 데이터입니다.
        """
        if index < 0:
            raise IndexError("인덱스는 음수일 수 없습니다.")
            
        # 리스트가 비어있고 인덱스가 0인 경우
        if self.is_empty():
            if index == 0:
                self.append(data)
            else:
                raise IndexError("빈 리스트에는 0번 인덱스에만 삽입할 수 있습니다.")
            return

        # 맨 앞에 삽입하는 경우 (인덱스 0)
        if index == 0:
            self.prepend(data)
            return
        
        new_node = Node(data)
        current_node = self.last.next
        count = 0

        # 삽입 위치의 이전 노드를 찾기 위해 순회
        while count < index - 1:
            current_node = current_node.next
            count += 1
            if current_node == self.last.next: # 한 바퀴를 돌았는데도 인덱스를 못 찾음
                raise IndexError("인덱스가 리스트의 범위를 벗어났습니다.")
        
        # 중간 또는 끝에 삽입
        new_node.next = current_node.next
        current_node.next = new_node
        
        # 마지막 노드에 삽입한 경우 last 포인터 업데이트
        if current_node == self.last:
            self.last = new_node

    def delete(self, data):
        """
        특정 데이터를 가진 노드를 리스트에서 삭제합니다.
        
        Args:
            data: 삭제할 노드의 데이터입니다.
        """
        if self.is_empty():
            return

        current_node = self.last.next # 첫 번째 노드부터 시작합니다.
        prev_node = None

        while True:
            if current_node.data == data:
                # 리스트에 노드가 하나뿐인 경우
                if current_node == self.last and prev_node is None:
                    self.last = None
                    return
                # 헤드 노드를 삭제하는 경우
                if prev_node is None:
                    self.last.next = current_node.next
                # 마지막 노드를 삭제하는 경우
                elif current_node == self.last:
                    prev_node.next = self.last.next
                    self.last = prev_node
                # 중간 노드를 삭제하는 경우
                else:
                    prev_node.next = current_node.next
                return

            prev_node = current_node
            current_node = current_node.next
            
            if current_node == self.last.next:
                # 한 바퀴를 돌아서 다시 시작점으로 돌아오면 종료
                break

    def display(self):
        """
        리스트의 모든 노드를 순회하며 데이터를 출력합니다.
        """
        if self.is_empty():
            print("리스트가 비어 있습니다.")
            return

        elements = []
        current_node = self.last.next # 첫 번째 노드부터 시작
        
        while True:
            elements.append(current_node.data)
            current_node = current_node.next
            if current_node == self.last.next: # 다시 시작점으로 돌아오면 루프를 멈춤
                break
        print(" -> ".join(map(str, elements)))

# 순환 연결 리스트 사용 예제
if __name__ == '__main__':


    print("--- 단일 연결 리스트 ---")
    llist = LinkedList()
    llist.append(10)s
    llist.append(30)
    llist.display()  # 출력: 10 -> 30

    llist.insert_at(1, 20)
    llist.display()  # 출력: 10 -> 20 -> 30

    llist.insert_at(0, 5)
    llist.display()  # 출력: 5 -> 10 -> 20 -> 30
    
    llist.insert_at(4, 35)
    llist.display()  # 출력: 5 -> 10 -> 20 -> 30 -> 35
# 연결 리스트 사용 예제
    print("\n--- 순환 연결 리스트 (insert_at 추가) ---")
    cllist = CircularLinkedList()
    cllist.append(10)
    cllist.append(30)
    cllist.display()  # 10 -> 30

    cllist.insert_at(1, 20)
    cllist.display()  # 10 -> 20 -> 30
    
    cllist.insert_at(0, 5)
    cllist.display()  # 5 -> 10 -> 20 -> 30
    
    cllist.insert_at(4, 40)
    cllist.display()  # 5 -> 10 -> 20 -> 30 -> 40
    
    cllist.insert_at(2, 15)
    cllist.display()  # 5 -> 10 -> 15 -> 20 -> 30 -> 40
    
    try:
        cllist.insert_at(10, 100)
    except IndexError as e:
        print(f"오류: {e}") # 오류: 인덱스가 리스트의 범위를 벗어났습니다.

    try:
        cllist.insert_at(-1, -5)
    except IndexError as e:
        print(f"오류: {e}") # 오류: 인덱스는 음수일 수 없습니다.
