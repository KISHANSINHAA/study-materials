# ====================================================================
# THEORY & CONCEPT:
# Factorial of a non-negative integer n is the product of all positive integers less than or equal to n. It can be computed iteratively using a loop or recursively. The recursion bases itself on the relation: n! = n * (n-1)!
#
# COMPLEXITY:
# Time Complexity: O(N) as we multiply N times.
# Space Complexity: O(1) for iterative; O(N) call-stack space for recursive.
#
# INTERVIEW Q&A:
# Q: What is recursion limit in Python?
# A: Python has a default call-stack recursion limit of 1000 to prevent stack overflows. You can check/set it using sys.getrecursionlimit().
#
# Q: What is the factorial of 0?
# A: 0! is mathematically defined as 1.
# ====================================================================

# Python program to find the factorial of a number
# n! = n * (n-1) * (n-2) * ... * 1. Factorial of 0 is 1.

# Method 1: Iterative (O(N) time, O(1) space)
def factorial_iterative(n: int) -> int:
    """
    Calculates factorial using a loop.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Method 2: Recursive (O(N) time, O(N) call stack space)
def factorial_recursive(n: int) -> int:
    """
    Calculates factorial using recursion.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)

# Test cases
if __name__ == "__main__":
    num = 5
    print(f"Iterative factorial of {num}:", factorial_iterative(num))
    print(f"Recursive factorial of {num}:", factorial_recursive(num))
