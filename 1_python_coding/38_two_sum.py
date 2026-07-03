# ====================================================================
# THEORY & CONCEPT:
# Given an array, find two indices whose values sum to a target. Instead of a nested loop (O(N^2)), we use a Hash Map. As we iterate, we calculate the complement (target - current_val). If the complement is in our map, we have found the pair.
#
# COMPLEXITY:
# Time Complexity: O(N) single-pass lookup.
# Space Complexity: O(N) to store elements in the hash map.
#
# INTERVIEW Q&A:
# Q: What is the brute force time complexity of Two Sum?
# A: O(N^2) because it checks all possible pairs in the array.
#
# Q: Why does the Hash Map approach take O(N) space?
# A: In the worst case, we store all N elements in the dictionary before finding a match.
# ====================================================================

# Python program for Two Sum
# Problem: Find two numbers in an array that add up to a target sum.
# Best approach: Use a hash map to achieve O(N) time and O(N) space.

def two_sum(nums: list, target: int) -> list:
    """
    Returns indices of the two numbers that add up to target.
    """
    seen = {}  # val -> index
    for idx, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], idx]
        seen[num] = idx
    return []

# Test case
if __name__ == "__main__":
    arr = [2, 7, 11, 15]
    t = 9
    print(f"Array: {arr}, Target: {t}")
    print("Indices:", two_sum(arr, t))
