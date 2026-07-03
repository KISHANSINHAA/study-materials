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

# Python program to find the Longest Common Prefix in an array of strings

def longest_common_prefix(strs: list) -> str:
    """
    Finds the longest common prefix among strings.
    """
    if not strs:
        return ""
        
    # Sort the array. The common prefix of all strings must be a prefix of
    # the first and last sorted strings.
    strs = sorted(strs)
    first = strs[0]
    last = strs[-1]
    
    i = 0
    # Compare first and last string character by character
    while i < len(first) and i < len(last) and first[i] == last[i]:
        i += 1
        
    return first[:i]

# Test cases
if __name__ == "__main__":
    test_cases = [
        ["flower", "flow", "flight"],
        ["dog", "racecar", "car"],
        ["accenture", "accidental", "accord"]
    ]
    for case in test_cases:
        print(f"Words: {case} -> Prefix: '{longest_common_prefix(case)}'")
