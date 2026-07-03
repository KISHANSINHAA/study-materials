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

# Python program to check Armstrong Number
# An Armstrong number is a number that is equal to the sum of its own digits each raised to the power of the number of digits.
# Example: 153 = 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153.

def is_armstrong(n: int) -> bool:
    """
    Checks if n is an Armstrong number.
    """
    if n < 0:
        return False
        
    # Convert number to string to extract digits and length
    str_n = str(n)
    num_digits = len(str_n)
    
    # Calculate sum of digits raised to the power of num_digits
    digit_sum = sum(int(digit) ** num_digits for digit in str_n)
    
    return digit_sum == n

# Test cases
if __name__ == "__main__":
    test_nums = [153, 370, 371, 407, 9474, 123]
    for num in test_nums:
        print(f"Is {num} an Armstrong number? -> {is_armstrong(num)}")
