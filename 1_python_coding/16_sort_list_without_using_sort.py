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

# Python program to sort a list without using sort() or sorted()
# We will implement the Bubble Sort algorithm.

def bubble_sort(arr: list) -> list:
    """
    Sorts a list in-place using bubble sort.
    Time Complexity: O(N^2) worst/average, O(N) best case.
    """
    n = len(arr)
    # Copy array to preserve original
    sorted_arr = arr.copy()
    
    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swapped = True
        # If no elements were swapped in internal loop, then list is sorted
        if not swapped:
            break
            
    return sorted_arr

# Test cases
if __name__ == "__main__":
    unsorted = [64, 34, 25, 12, 22, 11, 90]
    print("Unsorted List:", unsorted)
    print("Sorted List:  ", bubble_sort(unsorted))
