# ====================================================================
# THEORY & CONCEPT:
# String mutability in Python: Strings are immutable, meaning any modification generates a new string. Python's slicing `[::-1]` executes via optimized C-level code, making it the most memory and time-efficient approach.
#
# COMPLEXITY:
# Time Complexity: O(N) to traverse the string.
# Space Complexity: O(N) to store the reversed string.
#
# INTERVIEW Q&A:
# Q: Why is slicing [::-1] faster than a loop?
# A: Slicing is executed as a single step in C-level memory, bypassing Python interpreter loop overhead.
#
# Q: Can you reverse a string in-place in Python?
# A: No, because strings in Python are immutable objects. Any reversal requires creating a new string.
# ====================================================================

# Python program to reverse a string
# We will show three common methods to reverse a string.

# Method 1: Slicing (Most Pythonic and fastest)
def reverse_string_slicing(s: str) -> str:
    """
    Reverses the string using slicing [start:stop:step] with step as -1.
    """
    return s[::-1]

# Method 2: Using built-in reversed() and join()
def reverse_string_reversed(s: str) -> str:
    """
    reversed() returns an iterator that yields characters in reverse order.
    "".join() joins them back into a single string.
    """
    return "".join(reversed(s))

# Method 3: Iterative loop (Classic programming approach)
def reverse_string_loop(s: str) -> str:
    """
    Builds the reversed string character by character from the end.
    """
    reversed_str = ""
    for char in s:
        reversed_str = char + reversed_str
    return reversed_str

# Test cases
if __name__ == "__main__":
    test_str = "Accenture Coding"
    print("Original String:", test_str)
    print("Method 1 (Slicing):", reverse_string_slicing(test_str))
    print("Method 2 (Reversed):", reverse_string_reversed(test_str))
    print("Method 3 (Loop):", reverse_string_loop(test_str))
