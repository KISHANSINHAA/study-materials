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

# Python program for Merge Sort (Basic)
# Merge sort is a divide-and-conquer algorithm with O(N log N) time complexity.

def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr
        
    # Find middle index
    mid = len(arr) // 2
    
    # Recursively sort left and right halves
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Merge sorted halves
    return merge(left, right)

def merge(left: list, right: list) -> list:
    merged = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    # Append leftover elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

# Test case
if __name__ == "__main__":
    nums = [38, 27, 43, 3, 9, 82, 10]
    print("Unsorted:", nums)
    print("Sorted (Merge Sort):", merge_sort(nums))
