"""Complete the Queue2 class so that it makes use of the head/tail pointers
Make sure you keep the new doctests given below.
"""
import doctest
import os

os.environ['TERM'] = 'linux'  # Suppress ^[[?1034h


class Node:
    """A node for a linked list."""

    def __init__(self, item):
        self.item = item
        self.next_node = None


class Queue2:
    """ Implements a Queue using a Linked List with head and tail pointers
    You should be able to copy a lot of your code from your Queue class
    but you will be able to make efficiency gains via the use of a tail pointer
    >>> q = Queue2()
    >>> len(q)
    0
    >>> print(q)
    Queue2: head/front -> None
    >>> result = q.dequeue()
    Traceback (most recent call last):
    ...
    IndexError: Can't dequeue from empty queue.
    >>> print(len(q))
    0
    >>> result2 = q.dequeue()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    IndexError: Can't dequeue from empty queue.
    >>> q.enqueue('a')
    >>> print(q)
    Queue2: head/front -> a -> None
    >>> print(q.tail.item)
    a
    >>> print(q.head.item)
    a
    >>> len(q)
    1
    >>> q.dequeue()
    'a'
    >>> len(q)
    0
    >>> q.enqueue('a')
    >>> q.enqueue('b')
    >>> print(q)
    Queue2: head/front -> a -> b -> None
    >>> q.enqueue('c')
    >>> print(q)
    Queue2: head/front -> a -> b -> c -> None
    >>> len(q)
    3
    >>> q.dequeue()
    'a'
    >>> print(q)
    Queue2: head/front -> b -> c -> None
    >>> q.enqueue('z')
    >>> print(q.head.item)
    b
    >>> print(q.tail.item)
    z
    >>> q.dequeue()
    'b'
    >>> q.dequeue()
    'c'
    >>> q.dequeue()
    'z'
    >>> print(q.head)
    None
    >>> print(q.tail)
    None
    """

    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, item):
        """Add an item onto the tail of the queue."""
        new_node = Node(item)
        if self.tail is None:  # empty queue
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next_node = new_node
            self.tail = new_node

    def dequeue(self):
        """Remove and return the item at the front of the queue.
        Raise IndexError if queue is empty.
        """
        if self.head is None:
            raise IndexError("Can't dequeue from empty queue.")
        item = self.head.item
        self.head = self.head.next_node
        if self.head is None:  # queue is now empty
            self.tail = None
        return item

    def __len__(self):
        """Return the number of items in the queue."""
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next_node
        return count
    def is_empty(self):
        """Return True if the queue is empty, else False."""
        return self.head is None

    def __str__(self):
        """Returns a string representation of the list for the queue
        starting from the beginning of the list.
        Items are separated by ->
        and ending with -> None
        eg, Queue2: head/front -> a -> b -> None
        See doctests in class docstring
        """
        result = 'Queue2: head/front'
        current = self.head
        while current is not None:
            result += ' -> ' + str(current.item)
            current = current.next_node
        result += ' -> None'
        return result


def main():
    """ Mainly tests """
    # set verbose to False to get less doctest output
    verbose = True

    # Can enter an infinite loop if Queue2 isn't implemented correctly
    result = doctest.testmod()
    if verbose:
        print(result)


if __name__ == '__main__':
    main()
