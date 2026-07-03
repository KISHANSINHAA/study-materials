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

# Python program to check if a year is a leap year
# Rules:
# 1. Divisible by 4
# 2. If divisible by 100, must also be divisible by 400.

def is_leap_year(year: int) -> bool:
    """
    Returns True if the year is a leap year, otherwise False.
    """
    if year % 4 == 0:
        if year % 100 == 0:
            return year % 400 == 0
        return True
    return False

# Test cases
if __name__ == "__main__":
    years = [2000, 2004, 1900, 2024, 2026]
    for yr in years:
        print(f"Is {yr} a leap year? -> {is_leap_year(yr)}")
