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

# Python program for Linear Search
# Linear search works on both sorted and unsorted arrays. Time complexity is O(N).

def linear_search(arr: list, target) -> int:
    """
    Scans the array sequentially to find the target.
    Returns the index if found, else -1.
    """
    for idx, element in enumerate(arr):
        if element == target:
            return idx
    return -1

# Test case
if __name__ == "__main__":
    items = [4, 2, 7, 1, 9, 3]
    t = 9
    print(f"List: {items}, Target: {t}")
    print("Index found at:", linear_search(items, t))
