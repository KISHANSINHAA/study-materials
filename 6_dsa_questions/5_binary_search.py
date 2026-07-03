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

# DSA Question: Binary Search
# Time: O(log N), Space: O(1)

def binary_search(nums: list, target: int) -> int:
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

if __name__ == "__main__":
    print(binary_search([1, 3, 5, 7, 9], 7)) # Index 3
