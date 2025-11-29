class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
class Linked_list:
    def __init__(self):
        self.head = None
    def __len__(self):
        cnt = 0
        current = self.head
        while current:
            current = current.next
            cnt += 1
        return cnt
    def insert(self,data):
        new_node = Node(data)
        if self.head == None:
            self.head == new_node
            return
        if self.head:
            
            
            