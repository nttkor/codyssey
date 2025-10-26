class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.cnt = 0

    def __len__(self) -> int:
        return self.cnt
    def display(self):
        if self.cnt == 0:
            print("Empty")
        else:
            current = self.head
            for _ in range(self.cnt):
                print(current.data,end='->')
                current = current.next
            print()

    def to_list(self):
        current = self.head
        list_list = []
        for _ in range(self.cnt):
            list.append(current.data)
            current = current.next
        return list_list


    def insert(self, index, value):
        if index < 0 or index > len(self):
            raise IndexError("Index out of range")

        new_node = Node(value)
        self.cnt += 1

        # 맨 앞 삽입
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            prev = self.head
            for _ in range(index-1):
                prev = prev.next
            new_node.next = prev.next
            prev.next = new_node
        

ll = LinkedList()
ll.insert(0,1)
ll.insert(0,2)
ll.display()
print(ll.to_list)


    

