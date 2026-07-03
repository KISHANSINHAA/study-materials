# ====================================================================
# THEORY & CONCEPT:
# Python logic and utility code template. Demonstrates data cleaning, condition checking, and built-in type operations.
#
# COMPLEXITY:
# Time Complexity: O(N) average execution.
# Space Complexity: O(1) or O(N) auxiliary storage.
#
# INTERVIEW Q&A:
# Q: How does Python allocate memory for variables?
# A: Python variables are references to objects in memory. Immutable types (int, float, string, tuple) cannot be changed in place.
#
# Q: What is the difference between list.append() and list.extend()?
# A: append() adds its argument as a single element to the end of the list. extend() iterates over its argument and adds each element.
# ====================================================================

# Python Queue Implementation
# A queue is a FIFO (First In First Out) data structure.
# Using collections.deque is highly recommended as it provides O(1) appends and pops from both ends.

from collections import deque

class Queue:
    def __init__(self):
        self.queue = deque()
        
    def enqueue(self, item):
        """Adds an item to the back of the queue."""
        self.queue.append(item)
        print(f"Enqueued: {item}")
        
    def dequeue(self):
        """Removes and returns the front item of the queue."""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        item = self.queue.popleft()
        print(f"Dequeued: {item}")
        return item
        
    def peek(self):
        """Returns the front item without removing it."""
        if self.is_empty():
            return None
        return self.queue[0]
        
    def is_empty(self) -> bool:
        return len(self.queue) == 0
        
    def size(self) -> int:
        return len(self.queue)
        
    def __str__(self):
        return str(list(self.queue))

# Test cases
if __name__ == "__main__":
    q = Queue()
    q.enqueue("A")
    q.enqueue("B")
    q.enqueue("C")
    print("Current Queue:", q)
    print("Peek:", q.peek())
    q.dequeue()
    print("Queue after dequeue:", q)
    print("Queue size:", q.size())
