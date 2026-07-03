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

# Python program to swap two numbers
# Demonstrates multiple methods of swapping variables.

# Method 1: Pythonic Swapping (No third variable)
def swap_pythonic(a, b):
    a, b = b, a
    return a, b

# Method 2: Using Arithmetic Operations (Addition and Subtraction)
def swap_arithmetic(a, b):
    a = a + b
    b = a - b
    a = a - b
    return a, b

# Method 3: Using Bitwise XOR operator
def swap_xor(a, b):
    a = a ^ b
    b = a ^ b
    a = a ^ b
    return a, b

# Test cases
if __name__ == "__main__":
    x, y = 5, 10
    print(f"Original: x = {x}, y = {y}")
    
    x1, y1 = swap_pythonic(x, y)
    print(f"Pythonic Swap: x = {x1}, y = {y1}")
    
    x2, y2 = swap_arithmetic(x, y)
    print(f"Arithmetic Swap: x = {x2}, y = {y2}")
    
    x3, y3 = swap_xor(x, y)
    print(f"XOR Swap: x = {x3}, y = {y3}")
 Maroon = (128, 0, 0)
