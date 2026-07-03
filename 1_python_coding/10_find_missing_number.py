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

# Python program to find the missing number in an array
# Problem: Given an array containing n-1 integers in the range [1, n]. Find the missing number.

def find_missing_number(arr: list, n: int) -> int:
    """
    Finds the missing number using the sum formula: Sum = n * (n + 1) / 2.
    Time Complexity: O(N), Space Complexity: O(1).
    """
    expected_sum = (n * (n + 1)) // 2
    actual_sum = sum(arr)
    return expected_sum - actual_sum

def find_missing_number_xor(arr: list, n: int) -> int:
    """
    Finds the missing number using XOR.
    Avoids potential overflow issues in languages with fixed integer sizes.
    """
    xor_all = 0
    # XOR all numbers from 1 to n
    for i in range(1, n + 1):
        xor_all ^= i
    # XOR all elements in the array
    xor_arr = 0
    for num in arr:
        xor_arr ^= num
        
    return xor_all ^ xor_arr

# Test case
if __name__ == "__main__":
    # Missing number is 4. Array length is 5 (n=6)
    arr = [1, 2, 3, 5, 6]
    n = 6
    print(f"Array: {arr}, Range: 1 to {n}")
    print("Missing Number (Sum Method):", find_missing_number(arr, n))
    print("Missing Number (XOR Method):", find_missing_number_xor(arr, n))
