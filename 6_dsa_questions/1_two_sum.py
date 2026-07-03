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

# DSA Question: Two Sum
# Time: O(N), Space: O(N) using HashMap

def two_sum(nums: list, target: int) -> list:
    hashmap = {}
    for idx, num in enumerate(nums):
        diff = target - num
        if diff in hashmap:
            return [hashmap[diff], idx]
        hashmap[num] = idx
    return []

if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))
