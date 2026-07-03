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

# DSA Question: Longest Substring Without Repeating Characters
# Time: O(N), Space: O(min(m, n)) using Sliding Window

def length_of_longest_substring(s: str) -> int:
    char_map = {} # char -> index
    max_len = 0
    start = 0
    
    for end, char in enumerate(s):
        # If character is repeating and lies within current sliding window
        if char in char_map and char_map[char] >= start:
            start = char_map[char] + 1
        
        char_map[char] = end
        max_len = max(max_len, end - start + 1)
        
    return max_len

if __name__ == "__main__":
    print(length_of_longest_substring("abcabcbb")) # 3 ("abc")
    print(length_of_longest_substring("bbbbb"))    # 1 ("b")
