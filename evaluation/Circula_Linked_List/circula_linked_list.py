class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class circularlist:
    def __init__(self):
        self.cursor = None   # 현재 위치 (head 역할)
        self._size = 0

    def is_empty(self):
        return self._size == 0

    # -----------------------------------------
    # 마지막 노드 반환
    # -----------------------------------------
    def last(self):
        if self.is_empty():
            return None

        cur = self.cursor
        while cur.next != self.cursor:
            cur = cur.next
        return cur

    # -----------------------------------------
    # insert(value)
    # - empty: 단일 원형 생성
    # - else : cursor 뒤 삽입 후 cursor 이동
    # -----------------------------------------
    def insert(self, value):
        new_node = Node(value)

        if self.is_empty():
            new_node.next = new_node
            self.cursor = new_node
            self._size = 1
            return

        # cursor 뒤에 삽입
        new_node.next = self.cursor.next
        self.cursor.next = new_node

        # cursor 이동
        self.cursor = new_node
        self._size += 1

    # -----------------------------------------
    # get_next()
    # -----------------------------------------
    def get_next(self):
        if self.is_empty():
            return None

        self.cursor = self.cursor.next
        return self.cursor.value

    # -----------------------------------------
    # search(value)
    # -----------------------------------------
    def search(self, value):
        if self.is_empty():
            return False

        cur = self.cursor
        for _ in range(self._size):
            if cur.value == value:
                return True
            cur = cur.next
        return False

    # -----------------------------------------
    # delete(value)
    # - 첫 발견 노드 삭제
    # - 삭제 대상이 cursor인 경우 last()로 prev 찾기
    # -----------------------------------------
    def delete(self, value):
        if self.is_empty():
            return False

        cur = self.cursor
        prev = None

        for _ in range(self._size):
            if cur.value == value:

                # 노드 1개만 있는 경우
                if self._size == 1:
                    self.cursor = None
                    self._size = 0
                    return True

                # prev가 없는 경우 -> 삭제 대상이 cursor
                if prev is None:
                    prev = self.last()

                # 연결 끊기
                prev.next = cur.next

                # cursor가 삭제되면 cursor 이동
                if cur is self.cursor:
                    self.cursor = prev.next

                self._size -= 1
                return True

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
        cur = self.cursor
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
    

    
