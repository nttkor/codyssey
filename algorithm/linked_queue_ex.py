class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class Linked_list:
    def __init__(self):
        self.head = None
    def append(self, data):
        newnode = Node(data)
        if not self.head:
            self.head = newnode
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = newnode
    def display(self):
        current = self.head
        while current:
            print(current.data,end = ' -> ')
            current = current.next
        print('END')
    def delete(self,key):
        if not self.head:
            return
        current = self.head
        prev = None
        while current:
            if current and current.data != key:
                current = current.next
            
                

ll=Linked_list()
for i in range(5):
    ll.append(i)
    ll.delete(0)
    ll.delete(2)
    ll.display()
            
            
        
        
    
        
        