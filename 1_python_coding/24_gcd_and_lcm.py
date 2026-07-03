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

# Python program to find GCD (Greatest Common Divisor) and LCM (Least Common Multiple)
# Uses Euclidean Algorithm for GCD.

def find_gcd(a: int, b: int) -> int:
    """
    Computes GCD using Euclidean division method.
    """
    while b:
        a, b = b, a % b
    return a

def find_lcm(a: int, b: int) -> int:
    """
    Computes LCM using formula: LCM(a, b) = (a * b) / GCD(a, b)
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // find_gcd(a, b)

# Test cases
if __name__ == "__main__":
    n1, n2 = 12, 18
    print(f"Numbers: {n1}, {n2}")
    print("GCD:", find_gcd(n1, n2))
    print("LCM:", find_lcm(n1, n2))
