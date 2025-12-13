class Node:
    def __init__(self, value):
        self.value = value
        self.next : Node | None= None
class CircularLinkedList:
    def __init__(self):
        self.cursor : Node | None= None
        self.size = 0
    def insert(self, value) -> None:
        new_node = Node(value)
        if self.cursor is None:
            new_node.next = new_node
            self.cursor = new_node
        else:
            new_node.next = self.cursor.next