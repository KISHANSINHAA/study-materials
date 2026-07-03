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

# Python program to find the union of two arrays

def array_union(arr1: list, arr2: list) -> list:
    """
    Returns a sorted list representing the union of two arrays (unique values).
    """
    return sorted(list(set(arr1) | set(arr2)))

# Test case
if __name__ == "__main__":
    a1 = [1, 2, 3, 4]
    a2 = [3, 4, 5, 6]
    print(f"Array 1: {a1}")
    print(f"Array 2: {a2}")
    print("Union:   ", array_union(a1, a2))
