class Node:
    def __init__(self, data):
        self.data = data
        self.next : Node | None = None

class LinkedList:
    def __init__(self):
        self.head : Node | None = None
        self.tail : Node | None = None
        self.length = 0
    def __len__(self) -> int:
        return self.length
    def display(self):
        if self.length == 0:
            print("Empty")
        else:
            current = self.head
            while current:
                print(current.data,end='->')
            current = current.next
            print()
    def to_list(self):
        current = self.head
        list_list = []
        while current:
            list_list.append(current.data)
            current = current.next
        return list_list
    def insert(self, index: int, value: int) -> None:
        if index <- or index > len(self):
            raise IndexError
        new_node = Node(value)
        self.length += 1
        if index == 0:
            new_node.next = self.head
            self.head = new_node
            if self.length == 1:
                self.tail = new_node
        else:
            
            
