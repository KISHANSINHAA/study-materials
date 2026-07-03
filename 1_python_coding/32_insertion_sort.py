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

# Python program for Insertion Sort
# Insertion sort builds the final sorted list one item at a time by inserting elements in their correct position.

def insertion_sort(arr: list) -> list:
    n = len(arr)
    sorted_arr = arr.copy()
    
    for i in range(1, n):
        key = sorted_arr[i]
        # Move elements of sorted_arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        j = i - 1
        while j >= 0 and sorted_arr[j] > key:
            sorted_arr[j + 1] = sorted_arr[j]
            j -= 1
        sorted_arr[j + 1] = key
        
    return sorted_arr

# Test case
if __name__ == "__main__":
    nums = [12, 11, 13, 5, 6]
    print("Unsorted:", nums)
    print("Sorted (Insertion Sort):", insertion_sort(nums))
