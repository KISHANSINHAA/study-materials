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

# Python program to find duplicate elements in a list

def find_duplicates(arr: list) -> list:
    """
    Returns a list of duplicate items in the input list.
    Runs in O(N) time using sets.
    """
    seen = set()
    duplicates = set()
    for item in arr:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

# Test cases
if __name__ == "__main__":
    nums = [1, 2, 3, 2, 4, 5, 1, 6, 2]
    print(f"Original: {nums}")
    print(f"Duplicate Elements: {find_duplicates(nums)}")
