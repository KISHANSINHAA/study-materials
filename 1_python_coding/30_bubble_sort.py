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

# Python program for Bubble Sort
# Bubble sort compares adjacent elements and swaps them if they are in the wrong order.

def bubble_sort(arr: list) -> list:
    n = len(arr)
    sorted_arr = arr.copy()
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swapped = True
        if not swapped:
            break
    return sorted_arr

# Test case
if __name__ == "__main__":
    nums = [64, 34, 25, 12, 22, 11, 90]
    print("Unsorted:", nums)
    print("Sorted (Bubble Sort):", bubble_sort(nums))
