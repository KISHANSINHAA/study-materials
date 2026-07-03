# ====================================================================
# THEORY & CONCEPT:
# A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself. To check if a number N is prime, we only need to test divisors up to the square root of N, since any factor larger than sqrt(N) must have a corresponding factor smaller than sqrt(N).
#
# COMPLEXITY:
# Time Complexity: O(sqrt(N)) since we loop up to sqrt(N).
# Space Complexity: O(1) auxiliary space.
#
# INTERVIEW Q&A:
# Q: Why is checking up to sqrt(N) sufficient?
# A: If a number N has a factor a * b = N, and both a and b were greater than sqrt(N), then a * b would exceed N. Thus, at least one factor must be <= sqrt(N).
#
# Q: Is 1 a prime number?
# A: No, by definition, prime numbers must be integers strictly greater than 1.
# ====================================================================

# Python program to check if a number is prime
# A prime number is a number greater than 1 that has no positive divisors other than 1 and itself.

import math

def is_prime(n: int) -> bool:
    """
    Checks if n is prime in O(sqrt(n)) time.
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:  # Exclude even numbers greater than 2
        return False
        
    # Check divisors up to square root of n
    # Increment by 2 to check only odd numbers
    limit = int(math.isqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True

# Test cases
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 17, 20, 97, 100]
    for num in numbers:
        print(f"Is {num} prime? -> {is_prime(num)}")
