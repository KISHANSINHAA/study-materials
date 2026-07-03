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

# Python program to find the first non-repeating character in a string

def first_uniq_char(s: str) -> int:
    """
    Returns the index of the first non-repeating character, or -1 if none exists.
    """
    # Count frequencies
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
        
    # Find the first character with count 1
    for idx, char in enumerate(s):
        if freq[char] == 1:
            return idx
    return -1

# Test cases
if __name__ == "__main__":
    texts = ["leetcode", "loveleetcode", "aabb"]
    for t in texts:
        idx = first_uniq_char(t)
        char = t[idx] if idx != -1 else "None"
        print(f"String: '{t:12}' -> First non-repeating character: '{char}' at index {idx}")
