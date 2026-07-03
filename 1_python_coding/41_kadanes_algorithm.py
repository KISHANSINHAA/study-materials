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

# Python program for Kadane's Algorithm
# Finds the contiguous subarray within a 1D numerical array that has the largest sum.
# Time Complexity: O(N), Space Complexity: O(1).

def max_subarray_sum(nums: list) -> int:
    """
    Calculates max subarray sum using Kadane's Algorithm.
    """
    if not nums:
        return 0
        
    max_so_far = nums[0]
    current_max = nums[0]
    
    for num in nums[1:]:
        # Decide whether to add current element to existing subarray
        # or start a new subarray from current element
        current_max = max(num, current_max + num)
        max_so_far = max(max_so_far, current_max)
        
    return max_so_far

# Test case
if __name__ == "__main__":
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print("Array:", arr)
    print("Maximum Subarray Sum:", max_subarray_sum(arr))
