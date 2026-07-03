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

# Python program for Selection Sort
# Selection sort repeatedly finds the minimum element from the unsorted part and puts it at the beginning.

def selection_sort(arr: list) -> list:
    n = len(arr)
    sorted_arr = arr.copy()
    
    for i in range(n):
        min_idx = i
        # Find the minimum element in remaining unsorted array
        for j in range(i + 1, n):
            if sorted_arr[j] < sorted_arr[min_idx]:
                min_idx = j
                
        # Swap the found minimum element with the first element of unsorted part
        sorted_arr[i], sorted_arr[min_idx] = sorted_arr[min_idx], sorted_arr[i]
        
    return sorted_arr

# Test case
if __name__ == "__main__":
    nums = [29, 10, 14, 37, 13]
    print("Unsorted:", nums)
    print("Sorted (Selection Sort):", selection_sort(nums))
