# ====================================================================
# THEORY & CONCEPT:
# Binary search is an efficient divide-and-conquer algorithm to find a target value in a sorted array. It compares the target with the middle element of the array. If they differ, the half in which the target cannot lie is eliminated, reducing the search space by half.
#
# COMPLEXITY:
# Time Complexity: O(log N) as search space halves at each step.
# Space Complexity: O(1) for iterative; O(log N) for recursive call-stack.
#
# INTERVIEW Q&A:
# Q: What is the primary requirement of Binary Search?
# A: The input array must be sorted.
#
# Q: Why is Binary Search faster than Linear Search?
# A: Binary Search runs in logarithmic time O(log N), meaning for 1 million elements, it takes at most 20 comparisons, while Linear Search takes up to 1 million.
# ====================================================================

# Python program for Binary Search
# Binary search requires a sorted array. Time complexity is O(log N).

def binary_search_iterative(arr: list, target) -> int:
    """
    Performs iterative binary search on a sorted array.
    Returns index of target if found, else -1.
    """
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            
    return -1

def binary_search_recursive(arr: list, target, low: int, high: int) -> int:
    """
    Performs recursive binary search.
    """
    if low > high:
        return -1
        
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)

# Test cases
if __name__ == "__main__":
    sorted_arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target_val = 23
    print("Array:", sorted_arr)
    print("Target:", target_val)
    print("Index (Iterative):", binary_search_iterative(sorted_arr, target_val))
    print("Index (Recursive):", binary_search_recursive(sorted_arr, target_val, 0, len(sorted_arr) - 1))
