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

# DSA Question: Merge Sorted Arrays
# Time: O(m + n), Space: O(1) if merging back into nums1.

def merge_sorted(nums1: list, m: int, nums2: list, n: int) -> None:
    # Merges nums2 into nums1 in-place. nums1 has a length of m + n.
    # Start pointers from the end of both lists
    p1 = m - 1
    p2 = n - 1
    # Pointer for write location
    p = m + n - 1
    
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
        
    # If nums2 still has items, copy them
    if p2 >= 0:
        nums1[:p2 + 1] = nums2[:p2 + 1]

if __name__ == "__main__":
    nums1 = [1, 2, 3, 0, 0, 0]
    nums2 = [2, 5, 6]
    merge_sorted(nums1, 3, nums2, 3)
    print("Merged Array:", nums1)
