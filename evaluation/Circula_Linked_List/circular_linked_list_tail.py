class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class circularlist:
    def __init__(self):
        self.tail = None     # tail만 유지 (cursor는 tail.next로 계산)
        self._size = 0

    def is_empty(self):
        return self._size == 0

    # ----------------------------------------------------------
    # cursor = self.tail.next 를 반환하는 helper
    # ----------------------------------------------------------
    def _cursor(self):
        if self.is_empty():
            return None
        return self.tail.next

    # ----------------------------------------------------------
    # insert(value)
    #   - empty: 단일 원형 생성 (tail=노드)
    #   - else : tail 뒤에 삽입 후 tail=새 노드 이동
    # ----------------------------------------------------------
    def insert(self, value):
        new_node = Node(value)

        if self.is_empty():
            new_node.next = new_node     # 단일 원형
            self.tail = new_node
            self._size = 1
            return

        # tail 뒤 삽입 (cursor = tail.next)
        new_node.next = self.tail.next
        self.tail.next = new_node
        self.tail = new_node             # tail 이동
        self._size += 1

    # ----------------------------------------------------------
    # get_next()
    #   - empty → None
    #   - else → cursor를 한 칸 이동 (tail = tail.next)
    # ----------------------------------------------------------
    def get_next(self):
        if self.is_empty():
            return None

        # tail을 한 칸 이동 → cursor가 next가 되도록 유지
        self.tail = self.tail.next
        return self.tail.next.value      # cursor.next.value

    # ----------------------------------------------------------
    # search(value)
    # ----------------------------------------------------------
    def search(self, value):
        if self.is_empty():
            return False

        cur = self.tail.next  # cursor(head)
        for _ in range(self._size):
            if cur.value == value:
                return True
            cur = cur.next
        return False

    # ----------------------------------------------------------
    # delete(value)
    #   - head(cursor=tail.next) 삭제: prev=tail
    #   - tail 삭제: tail 갱신 필요
    #   - 중간 삭제: prev 찾아서 연결
    # ----------------------------------------------------------
    def delete(self, value):
        if self.is_empty():
            return False

        prev = self.tail
        cur = self.tail.next   # cursor(head)

        for _ in range(self._size):
            if cur.value == value:

                # 노드가 1개일 때
                if self._size == 1:
                    self.tail = None
                    self._size = 0
                    return True

                # 일반 삭제: prev.next 건너뛰기
                prev.next = cur.next

                # tail 삭제면 tail 이동
                if cur is self.tail:
                    self.tail = prev

                self._size -= 1
                return True

            prev = cur
            cur = cur.next

        return False

    # ----------------------------------------------------------
    # display()
    # ----------------------------------------------------------
    def display(self):
        if self.is_empty():
            print("[]")
            return

        result = []
        cur = self.tail.next   # cursor(head)
        for _ in range(self._size):
            result.append(str(cur.value))
            cur = cur.next

        print(" → ".join(result) + " (circular)")


# ----------------------------------------------------------
# 사용 예시 (필요 시 테스트용)
# ----------------------------------------------------------
if __name__ == "__main__":
    cl = circularlist()
    for i in range(10,60,10):
        cl.insert(i)
        cl.display()  # 10 → 20 → 30

    print("get_next:", cl.get_next())  # rotate
    cl.display()

    print("search 20:", cl.search(20))
    print("delete 10:", cl.delete(10))
    cl.display()

    print("delete 30:", cl.delete(30))
    cl.display()

    print("delete 20:", cl.delete(20))
    cl.display()
