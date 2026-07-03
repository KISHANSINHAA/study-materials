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

# DSA Question: Move Zeroes
# Time: O(N), Space: O(1) in-place pointer swap

def move_zeroes(nums: list) -> None:
    # insert_pos tracks position to insert next non-zero element
    insert_pos = 0
    for idx in range(len(nums)):
        if nums[idx] != 0:
            nums[insert_pos], nums[idx] = nums[idx], nums[insert_pos]
            insert_pos += 1

if __name__ == "__main__":
    arr = [0, 1, 0, 3, 12]
    move_zeroes(arr)
    print("Moved Zeroes:", arr) # [1, 3, 12, 0, 0]
