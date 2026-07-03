# ====================================================================
# THEORY & CONCEPT:
# Classic Data Structure and Algorithm problem. Focuses on spatial optimization, indexing, and temporal efficiencies.
#
# COMPLEXITY:
# Time Complexity: Optimized bound.
# Space Complexity: Minimized auxiliary footprint.
#
# INTERVIEW Q&A:
# Q: What is space-time trade-off?
# A: Designing algorithms to consume more memory (space) to run faster (time), or vice versa.
#
# Q: What is the time complexity of dictionary operations?
# A: Dictionary key insertions, deletions, and lookups take O(1) time on average.
# ====================================================================

# DSA Question: Rotate Array
# Time: O(N), Space: O(1) using reversing

def rotate(nums: list, k: int) -> None:
    n = len(nums)
    k = k % n
    
    def reverse(start, end):
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1
            
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)

if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5, 6, 7]
    rotate(arr, 3)
    print("Rotated Array:", arr) # [5, 6, 7, 1, 2, 3, 4]
