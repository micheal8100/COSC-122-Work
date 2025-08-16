class Node:
    def __init__(self, item, next_node=None):
        self.item = item
        self.next_node = next_node

class Stack:
    def __init__(self):
        self.head = None

    def push(self, item):
        new_node = Node(item, self.head)
        self.head = new_node
s = Stack()
s.push(10)
print(s.head.item)  # Should print 10
s.push(20)
print(s.head.item)  # Should print 20
print(s.head.next_node.item)  # Should print 10