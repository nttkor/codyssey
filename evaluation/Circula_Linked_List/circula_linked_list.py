class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class circularlist:
    def __init__(self):
        self._cursor = None     # 첫 노드를 나타내는 cursor
        self._size = 0

    def is_empty(self):
        return self._size == 0

    # --------------------------------------
    # insert(value)
    # 비었을 경우 Case 1: 빈 리스트 → 자기 자신을 가리키는 단일 원형 생성
    # ase 2: 커서 뒤에 삽입하고 cursor를 새 노드로 이동
    # --------------------------------------
    def insert(self, value):
        new_node = Node(value)

        # Case 1: 빈 리스트 → 자기 자신을 가리키는 단일 원형 생성
        if self.is_empty():
            new_node.next = new_node
            self._cursor = new_node
            self._size = 1
            return

        # Case 2: 커서 뒤에 삽입하고 cursor를 새 노드로 이동
        new_node.next = self._cursor.next
        self._cursor.next = new_node
        self._cursor = new_node   # cursor 이동
        self._size += 1

    # --------------------------------------
    # get_next()
    # --------------------------------------
    def get_next(self):
        if self.is_empty():
            return None

        self._cursor = self._cursor.next
        return self._cursor.value

    # --------------------------------------
    # search(value)
    # --------------------------------------
    def search(self, value):
        if self.is_empty():
            return False

        cur = self._cursor
        for _ in range(self._size):
            if cur.value == value:
                return True
            cur = cur.next
        return False

    # --------------------------------------
    # delete(value)
    # --------------------------------------
    def delete(self, value):
        if self.is_empty():
            return False

        cur = self._cursor
        prev = None

        # prev를 찾기 위해 전체 순회
        for _ in range(self._size):
            if cur.value == value:
                # 삭제 처리

                # Case: 노드 1개
                if self._size == 1:
                    self._cursor = None
                    self._size = 0
                    return True

                # prev가 없다면(첫 루프에서 cursor가 value인 경우)
                # → 원형 전체 돌며 prev를 찾아야 한다
                if prev is None:
                    prev = cur
                    for _ in range(self._size - 1):
                        prev = prev.next

                # 연결 해제
                prev.next = cur.next

                # 삭제 대상이 cursor면 cursor를 이전 노드로 이동
                if cur is self._cursor:
                    self._cursor = prev

                self._size -= 1
                return True

            # 다음 노드로 이동
            prev = cur
            cur = cur.next

        return False

    # --------------------------------------
    # display()
    # --------------------------------------
    def display(self,msg):
        print(msg,'len:'+f'{self._size}>>',end=' ')
        if self.is_empty():
            print("[]")
            return

        result = []
        cur = self._cursor
        for _ in range(self._size):
            result.append(str(cur.value))
            cur = cur.next

        print(" → ".join(result) + " (circular)")


# -----------------------------
# 사용 예시
# -----------------------------
if __name__ == "__main__":
    cl = circularlist()
    print(cl.delete(10))
    for i in range(10,60,10):
        cl.insert(i)
        cl.display('cl.insert({i})')


    print("next:", cl.get_next())
    print("next:", cl.get_next())
    print("search 20:", cl.search(20))
    for i in range(20,50,10):
        print(cl.delete(i))
        cl.display(f'delete({i})')
    for i in [10,50,50]:
        print(cl.delete(i))
        cl.display(f'delete({i})')
    

    
