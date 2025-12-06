#custom 함수 시작

def show_linked(llist):
    print(f"현재 리스트: {llist.to_list()}")
    print(f"현재 리스트 길이: {len(llist)}")


def show_cirlist(clist):
    print(f"현재 리스트: {clist.tolist()}")
    print(f"현재 리스트 길이: {clist.count}")





#custom 함수 끝



class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.count = 0

    def insert(self, index, value):
        if index < 0 or index > self.count:
            raise IndexError
        new_node = Node(value)
        if index == 0:
            new_node.next = self.head
            self.head = new_node

        else:
            node = self.head
            for _ in range(index-1):
                node = node.next
            new_node.next = node.next
            node.next = new_node
        self.count += 1

    
    def __len__(self):
        return self.count
    
    def to_list(self):
        result = []
        node = self.head
        while node:
            result.append(node.value)
            node = node.next

        return result
    
    def delete(self, index):
        if index < 0 or index >= self.count:
            raise IndexError
        if self.count == 0:
            value = self.head.value
            self.head = None
            self.count -= 1
            return value
        if index == 0:
            value = self.head.value
            self.head = self.head.next
            self.count -= 1
            return value
        
        else:
            prev = self.head
            for _ in range(index-1):
                prev = prev.next

            value = prev.next.value
            prev.next = prev.next.next
            self.count -= 1
            return value
        
class CircularList:
    def __init__(self):
        self.cursor = None
        self.count = 0

    def get_next(self):
        if not self.cursor:
            return None
        else:
            for _ in range(self.count):
                self.cursor = self.cursor.next
                return self.cursor.value
            
    def search(self, value):
        if not self.cursor:
            return False
        else:
            node = self.cursor
            for _ in range(self.count):
                if node.value == value:
                    return True
                node = node.next
            return False

    def insert(self, value):
        new_node = Node(value)
        if not self.cursor:
            new_node.next = new_node #여기 실수 잦다 주의
            self.cursor = new_node
            self.count += 1
            return
        else:
            new_node.next = self.cursor.next
            self.cursor.next = new_node
            self.cursor = new_node
            self.count += 1
            return
        
    def delete(self, value):
        if not self.cursor:
            return False
        else:
            if self.count == 1:
                self.cursor = None
                self.count -= 1
                return True
            else:
                prev, curr = self.cursor, self.cursor.next
                for _ in range(self.count):
                    if curr.value == value:
                        prev.next = curr.next
                        if curr == self.cursor:
                            self.cursor = prev
                        self.count -= 1
                        return True
                    prev, curr = curr, curr.next
                return False

       #커스텀 method 시작
    def tolist(self):
        result = []
        #추가하기: 빈 clist를 읽을 경우
        if not self.cursor:
            return result
        node = self.cursor
        for _ in range(self.count):
            result.append(node.value)
            node = node.next
        return result
            
def main():
    print("HERE'S THE PROVING GROUND!!")



if __name__ == "__main__":
    main()