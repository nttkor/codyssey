class Node:  # 노드 클래스 정의
    def __init__(self, data):  # 생성자: 데이터 저장
        self.data = data       # 노드가 저장할 데이터
        self.next = None       # 다음 노드를 가리키는 포인터

class circularlist:  # 원형 연결 리스트 클래스 정의
    def __init__(self):  # 생성자: 리스트 초기화
        self.tail = None       # 마지막 노드를 가리키는 tail 포인터
        self.cnt = 0           # 노드 수를 추적하는 카운터

    def __len__(self):  # 리스트 길이 반환 함수
        return self.cnt        # O(1)로 노드 수 반환

    def insert(self, data):  # 노드 삽입 함수
        new_node = Node(data)  # 새 노드 생성

        if self.tail is None:  # 리스트가 비어 있을 경우
            new_node.next = new_node  # 자기 자신을 가리킴
            self.tail = new_node      # tail을 새 노드로 설정
        else:
            new_node.next = self.tail.next  # 새 노드가 head를 가리킴
            self.tail.next = new_node       # tail이 새 노드를 가리킴
            self.tail = new_node            # tail을 새 노드로 업데이트

        self.cnt += 1  # 노드 수 증가

    def delete(self, data):  # 노드 삭제 함수
        if self.tail is None:  # 빈 리스트일 경우
            raise IndexError("삭제할 항목이 존재하지 않습니다. 리스트가 비어 있습니다.")

        prev = self.tail       # 이전 노드 초기화
        current = self.tail.next  # 현재 노드를 head로 초기화

        while True:
            if current.data == data:  # 삭제할 데이터 찾음
                if current == self.tail and current.next == self.tail:  # 노드가 하나뿐일 경우
                    self.tail = None
                else:
                    prev.next = current.next  # 이전 노드가 현재 다음 노드를 가리킴
                    if current == self.tail:  # tail 노드를 삭제할 경우
                        self.tail = prev
                self.cnt -= 1  # 노드 수 감소
                return
            prev = current
            current = current.next
            if current == self.tail.next:  # 한 바퀴 돌았을 경우
                break

        raise IndexError(f"삭제할 항목 '{data}'이(가) 리스트에 없습니다.")  # 삭제 실패

    def get_all(self):  # 전체 노드 순회 함수
        if self.tail is None:  # 빈 리스트일 경우
            return []

        result = []
        current = self.tail.next  # head부터 시작
        while True:
            result.append(current.data)
            current = current.next
            if current == self.tail.next:  # 한 바퀴 돌았을 경우
                break
        return result

    def search(self, keyword):  # 검색 함수
        if self.tail is None:  # 빈 리스트일 경우
            return []

        result = []
        current = self.tail.next  # head부터 시작
        while True:
            if keyword.lower() in current.data.lower():  # 키워드 포함 여부 확인
                result.append(current.data)
            current = current.next
            if current == self.tail.next:  # 한 바퀴 돌았을 경우
                break
        return result
def main():
    playlist = circularlist()

    playlist.insert("NewJeans - ETA")
    playlist.insert("IVE - After LIKE")
    playlist.insert("LE SSERAFIM - Perfect Night")

    print("🎶 전체 곡 목록:", playlist.get_all())
    print("📏 곡 개수:", len(playlist))

    playlist.delete("IVE - After LIKE")
    print("🗑️ 삭제 후 목록:", playlist.get_all())

    print("🔍 'Night' 포함 곡:", playlist.search("Night"))

    # 예외 테스트
    # playlist.delete("BLACKPINK - DDU-DU DDU-DU")  # IndexError 발생

if __name__ == '__main__':
    main()
