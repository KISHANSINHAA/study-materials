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

# Python program to find the intersection of two arrays

def array_intersection(arr1: list, arr2: list) -> list:
    """
    Returns unique common elements in both arrays.
    """
    return list(set(arr1) & set(arr2))

def array_intersection_duplicates(arr1: list, arr2: list) -> list:
    """
    Returns intersection and preserves duplicates relative to their occurrences in both.
    """
    # Using hash map / frequency count
    freq1 = {}
    for num in arr1:
        freq1[num] = freq1.get(num, 0) + 1
        
    intersection = []
    for num in arr2:
        if freq1.get(num, 0) > 0:
            intersection.append(num)
            freq1[num] -= 1
    return intersection

# Test cases
if __name__ == "__main__":
    a1 = [1, 2, 2, 1]
    a2 = [2, 2]
    print(f"Array 1: {a1}, Array 2: {a2}")
    print("Unique Intersection:  ", array_intersection(a1, a2))
    print("Duplicate Intersection:", array_intersection_duplicates(a1, a2))
