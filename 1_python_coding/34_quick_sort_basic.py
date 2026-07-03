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

# Python program for Quick Sort (Basic)
# Quick sort uses divide-and-conquer and partitions arrays around a pivot.

def quick_sort(arr: list) -> list:
    """
    Recursive quicksort using list comprehensions (easy to understand version).
    """
    if len(arr) <= 1:
        return arr
        
    # Choose pivot (here, the middle element)
    pivot = arr[len(arr) // 2]
    
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# Test case
if __name__ == "__main__":
    nums = [10, 7, 8, 9, 1, 5]
    print("Unsorted:", nums)
    print("Sorted (Quick Sort):", quick_sort(nums))
