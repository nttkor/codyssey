class Node:
    def __init__(self, value):
        self.value = value
        self.next =None
class LinkedList:
    def __init__(self):
        self.head=None
    def __len__(self):
        cnt = 0
        current = self.head
        while current:
            cnt += 1
            current = current.next
        return cnt
    def __str__(self):
        current = self.head
        values = []
        while current :
            values.append(str(current.value))
            current = current.next
        return '->'.join(values)
            
        
        
    def append(self,value):
        new = Node(value)
        if self.head == None:
            self.head = new
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new
ll = LinkedList()
ll.append(1)
ll.append(2)
print(len(ll), ll)
                
        
        
        
