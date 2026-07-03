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

# Python Stack Implementation
# A stack is a LIFO (Last In First Out) data structure.

class Stack:
    def __init__(self):
        self.stack = []
        
    def push(self, item):
        """Adds an item to the top of the stack."""
        self.stack.append(item)
        print(f"Pushed: {item}")
        
    def pop(self):
        """Removes and returns the top item. Raises error if empty."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        item = self.stack.pop()
        print(f"Popped: {item}")
        return item
        
    def peek(self):
        """Returns the top item without removing it."""
        if self.is_empty():
            return None
        return self.stack[-1]
        
    def is_empty(self) -> bool:
        """Returns True if stack is empty, else False."""
        return len(self.stack) == 0
        
    def size(self) -> int:
        """Returns the number of elements in the stack."""
        return len(self.stack)
        
    def __str__(self):
        return str(self.stack)

# Test cases
if __name__ == "__main__":
    s = Stack()
    s.push(10)
    s.push(20)
    s.push(30)
    print("Current Stack:", s)
    print("Peek:", s.peek())
    s.pop()
    print("Stack size:", s.size())
    print("Is empty?", s.is_empty())
