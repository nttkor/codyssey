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

# 네가 정리한 개념은 이게 정답이다
# cursor는 고정된 head/tail이 아니라
# 현재 위치 포인터이고,
# get_next()를 호출하면 리스트를 순환하면서 결국 “head처럼 보이는 위치”를 가리키게 된다.

# head를 따로 보관할 필요 없음
# tail도 굳이 안 들고 있어도 됨
# cursor + get_next() 만으로 전체 순환과 기준점이 만들어짐
# 이게 이 과제의 의도에 가장 잘 맞는 해석이다.
# 시험 관점에서 중요한 포인트 (너는 이미 맞게 구현함)
# 채점 포인트는 보통 이 부분이다:

# ✅ insert가 cursor 뒤에 되는가
# ✅ insert 후 cursor 이동하는가
# ✅ delete가 cursor부터 순회하는가
# ✅ get_next가 cursor를 이동시키는가
# ✅ empty 상태 처리


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

    # ----------------------------
    # delete(value)
    # ----------------------------
    def delete(self,value):
        if self.cursor == None:
            return False
        prev = self.cursor
        while prev.next != self.cursor:
            prev = prev.next
        cur = self.cursor

        for _ in range(self._size):
            if cur.value == value:
                # 링크 제거
                prev.next = cur.next
                # cursor 삭제 → 이전 노드로 이동
                if cur is self.cursor:
                    self.cursor = prev
                self._size -= 1
                if self._size == 0:
                    self.cursor = None
                return True

            prev = cur
            cur = cur.next

        return False

    # ----------------------------
    # display()
    # ----------------------------
    def display(self):
        """
        현재 cursor 위치부터 리스트를 순회하여 값을 출력한다.
        - 비어 있으면 "[]" 출력
        - 출력 형식: "val1 → val2 → ... (circular)"
        주의: 이 display는 'cursor부터 시작'해서 출력하므로
              insert한 직후에는 가장 최근 삽입 노드부터 보이게 된다.
        """
        if self.is_empty():
            print("[]")
            return

        result = []
        cur = self.cursor
        for _ in range(self._size):
            result.append(str(cur.value))
            cur = cur.next

        print(" → ".join(result) + " (circular)")


# ----------------------------
# 간단한 동작 예시 (테스트)
# ----------------------------
if __name__ == "__main__":
    cl = circularlist()

    # 삽입 예시: insert는 cursor 뒤에 넣고 cursor는 새 노드를 가리킨다.
    for i in range(10,40,10):
        cl.insert(i)   # 리스트: 10 (cursor->10)
        cl.display()    # 출력: 10 (circular)
    for i in range(10,40,10):
        cl.insert(i)   # 리스트: 10 (cursor->10)
        cl.display()    # 출력: 10 (circular)

    # get_next 예시: cursor 한 칸 전진
    print("get_next ->", cl.get_next())  # cursor moves, 출력되는 값은 이동한 cursor의 value
    cl.display()

    # search 예시
    print("search 20 ->", cl.search(20))
    print("search 999 ->", cl.search(999))

    # delete 예시: cursor부터 순회하여 처음 만나는 값을 삭제
    print("delete 10 ->", cl.delete(10))  # 10을 찾아 삭제 (cursor 기준으로 첫 발견)
    cl.display()

    # 삭제: cursor가 가리키는 노드 삭제되는 경우
    # (위에서 cursor는 delete 이후에 prev.next로 갱신되었을 수 있음)
    print("delete 30 ->", cl.delete(30))
    cl.display()

    # 모든 노드 삭제
    print("delete 20 ->", cl.delete(20))
    cl.display()
