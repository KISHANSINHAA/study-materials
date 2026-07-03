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

# Python program to find common elements in two lists

def common_elements_set(l1: list, l2: list) -> list:
    """
    Uses set intersection to find common elements.
    O(N + M) time complexity.
    """
    return list(set(l1).intersection(set(l2)))

def common_elements_comprehension(l1: list, l2: list) -> list:
    """
    Uses list comprehension. O(N * M) time complexity.
    Preserves duplicates and order of first list.
    """
    return [item for item in l1 if item in l2]

# Test cases
if __name__ == "__main__":
    list1 = [1, 2, 3, 4, 5]
    list2 = [4, 5, 6, 7, 8]
    print("List 1:", list1)
    print("List 2:", list2)
    print("Common Elements (Set Intersection):", common_elements_set(list1, list2))
    print("Common Elements (List Comprehension):", common_elements_comprehension(list1, list2))
