# ====================================================================
# THEORY & CONCEPT:
# The Fibonacci sequence is defined by F(n) = F(n-1) + F(n-2) with F(0)=0 and F(1)=1. The iterative approach operates in O(N) time. The naive recursive approach runs in exponential O(2^N) time due to overlapping subproblems.
#
# COMPLEXITY:
# Time Complexity: O(N) for iterative; O(2^N) for naive recursive.
# Space Complexity: O(1) auxiliary space for iterative; O(N) for recursion stack.
#
# INTERVIEW Q&A:
# Q: What is the problem with naive recursion in Fibonacci?
# A: It performs redundant calculations of the same subproblems. For instance, F(5) calculates F(4) and F(3), but F(4) also calculates F(3) again.
#
# Q: How can recursion be optimized?
# A: Using memoization (storing computed values) or converting it to an iterative dynamic programming approach.
# ====================================================================

# Python program to generate Fibonacci Series
# F(n) = F(n-1) + F(n-2) with F(0) = 0 and F(1) = 1.

# Method 1: Iterative approach (O(N) time, O(N) space to store terms)
def generate_fibonacci_iterative(n: int) -> list:
    """
    Generates a list of Fibonacci numbers up to n terms.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    fib_series = [0, 1]
    while len(fib_series) < n:
        fib_series.append(fib_series[-1] + fib_series[-2])
    return fib_series

# Method 2: Recursive approach to get the N-th term (O(2^N) time without memoization)
def fibonacci_recursive(n: int) -> int:
    """
    Returns the n-th Fibonacci number (0-indexed).
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# Method 3: Generator approach (Memory efficient for large numbers of terms)
def fibonacci_generator(n: int):
    """
    Yields Fibonacci numbers one by one up to n terms.
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Test cases
if __name__ == "__main__":
    terms = 10
    print(f"Iterative Fibonacci series ({terms} terms):", generate_fibonacci_iterative(terms))
    print(f"10th Fibonacci term recursively (0-indexed):", fibonacci_recursive(9))
    print(f"Generator Fibonacci series ({terms} terms):", list(fibonacci_generator(terms)))
