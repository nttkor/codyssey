
class Node:
    """
    단일 연결 리스트 노드 (singly linked node)
    - value: 저장 데이터
    - next : 다음 노드를 가리키는 포인터 (원형 리스트이므로 마지막 노드의 next는 리스트의 어떤 노드도 될 수 있음)
    """
    def __init__(self, value):
        self.value = value
        self.next = None


class circularlist:
    """
    cursor 기반 단일 원형 연결 리스트 구현

    설계/정의 요약:
    - self.cursor : '현재 위치'를 가리키는 포인터. (문제에서 정의한 cursor)
                    insert() 후에는 항상 새로 삽입된 노드를 가리킨다.
                    get_next() 호출 시 cursor는 한 칸 앞으로 이동한다.
    - self._size : 리스트에 들어있는 노드 개수
    - last() : 필요할 때마다 마지막 노드를 순회로 찾아 반환한다 (tail 멤버를 따로 들고 있지 않음)
    - delete(value) : cursor부터 순회하여 "처음 만나는" value를 가진 노드를 삭제한다.
                       cursor가 삭제 대상이면 prev를 last()로 찾아 처리한다.
    """

    def __init__(self):
        # cursor는 리스트에서 '현재 위치'를 가리킴. 비어있으면 None.
        self.cursor = None
        # 노드 수(0이면 빈 리스트)
        self._size = 0

    def is_empty(self):
        """리스트 비어있는지 확인"""
        return self._size == 0

    def __len__(self):
        """파이썬스러운 길이 조회 지원 (optional)"""
        return self._size

    # ----------------------------
    # last()
    # ----------------------------
    def last(self):
        """
        리스트에서 '마지막 노드'를 반환한다.
        - 목적: delete에서 cursor가 삭제 대상일 때 이전(prev) 노드를 찾기 위함.
        - 동작: cursor부터 순회해서 cursor로 돌아오기 바로 직전 노드를 반환.
        - 반환: 마지막 Node 객체 또는 None (빈 리스트)
        """
        if self.is_empty():
            return None

        cur = self.cursor
        # cur.next != self.cursor 가 성립할 때까지 이동하면
        # 마지막 노드(cur)가 cursor를 가리키는 직전 노드가 된다.
        while cur.next != self.cursor:
            cur = cur.next
        return cur

    # ----------------------------
    # insert(value)
    # ----------------------------
    def insert(self, value):
        """
        cursor 뒤에 새 노드를 삽입하고, cursor를 새 노드로 이동시킨다.
        동작 규칙:
        - 리스트가 비어있다면 새 노드는 자기 자신을 가리키는 단일 원형이 되고 cursor는 그 노드를 가리킨다.
        - 비어있지 않다면, 새노드.next = cursor.next; cursor.next = 새노드; cursor = 새노드
        """
        new_node = Node(value)

        # 빈 리스트인 경우: new_node는 자기 자신을 가리킨다 (단일 원형)
        if self.is_empty():
            new_node.next = new_node  # 단일 원형 만들기
            self.cursor = new_node    # cursor는 유일한 노드를 가리킴
            self._size = 1
            return

        # 비어있지 않으면 cursor 뒤에 삽입
        # (1) 새 노드가 cursor의 다음을 가리키도록 함
        new_node.next = self.cursor.next
        # (2) cursor가 새 노드를 가리키도록 연결
        self.cursor.next = new_node
        # (3) 문제 조건: 삽입 후 cursor는 새 노드를 가리킨다
        self.cursor = new_node
        # (4) 크기 증가
        self._size += 1

    # ----------------------------
    # get_next()
    # ----------------------------
    def get_next(self):
        """
        cursor를 한 칸 앞으로 이동시키고(=cursor = cursor.next) 그 노드의 값을 반환한다.
        - 비어있으면 None 반환
        - 반환값: cursor가 이동한 후의 노드.value
        주의: cursor 자체가 '현재 위치'이므로 get_next는 cursor를 전진시킨다.
        """
        if self.is_empty():
            return None

        # cursor 이동
        self.cursor = self.cursor.next
        # 이동 후의 cursor 값 반환
        return self.cursor.value

    # ----------------------------
    # search(value)
    # ----------------------------
    def search(self, value):
        """
        cursor 위치부터 순환하면서 value 값이 존재하는지 검사.
        - 존재하면 True, 없으면 False 반환
        - 빈 리스트인 경우 False 반환
        """
        if self.is_empty():
            return False

        cur = self.cursor
        for _ in range(self._size):
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def delete(self,value):
        if self.cursor == None:
            return False
        prev = self.cursor
        while prev.next != cussor:
            prev = prev.next
        cur = self.cursor

        for _ in range(self._size):
            