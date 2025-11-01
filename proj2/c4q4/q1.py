class Node:  # 노드 클래스 정의
    def __init__(self, data):  # 생성자: 데이터 저장
        self.data = data       # 노드가 저장할 데이터
        self.next = None       # 다음 노드를 가리키는 포인터

class linkedlist:  # 연결 리스트 클래스 정의
    def __init__(self):  # 생성자: 리스트 초기화
        self.head = None  # 첫 노드를 가리키는 head 포인터

    def __len__(self):  # 리스트 길이 반환 함수
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def insert(self, data, position=None):  # 노드 삽입 함수
        if position is not None and (position < 0 or position > len(self)):  # 유효한 위치 확인
            raise IndexError("삽입 위치가 리스트 범위를 벗어났습니다.")

        new_node = Node(data)  # 유효성 통과 후 노드 생성

        if position == 0 or self.head is None:  # 첫 번째 위치 또는 빈 리스트일 경우
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        index = 0

        while current.next and (position is None or index < position - 1):  # 삽입 위치까지 이동
            current = current.next
            index += 1

        new_node.next = current.next
        current.next = new_node

    def delete(self, data):  # 노드 삭제 함수
        current = self.head
        prev = None

        while current:
            if current.data == data:
                if prev is None:
                    self.head = current.next  # 첫 노드 삭제
                else:
                    prev.next = current.next  # 중간 또는 마지막 노드 삭제
                return True
            prev = current
            current = current.next

        raise IndexError(f"삭제할 항목 '{data}'이(가) 리스트에 없습니다.")  # 삭제 실패

    def get_list(self):  # 리스트 전체 반환 함수
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
def main():
    # 연결 리스트 생성
    playlist = linkedlist()

    # 음악 추가
    playlist.insert("NewJeans - Super Shy")               # 첫 번째 항목
    playlist.insert("IVE - I AM")                         # 마지막 항목
    playlist.insert("LE SSERAFIM - UNFORGIVEN", 1)        # 중간 삽입

    # 현재 목록 출력
    print("🎶 현재 플레이리스트:", playlist.get_list())

    # 음악 삭제
    playlist.delete("IVE - I AM")

    # 삭제 후 목록 출력
    print("🗑️ 삭제 후 플레이리스트:", playlist.get_list())

    # 리스트 길이 확인
    print("📏 현재 리스트 길이:", len(playlist))

    # 예외 테스트 (주석 해제 시 IndexError 발생)
    # playlist.insert("BTS - Dynamite", 10)
    # playlist.delete("BLACKPINK - DDU-DU DDU-DU")

if __name__ == '__main__':
    main()
