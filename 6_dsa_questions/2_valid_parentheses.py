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

# DSA Question: Valid Parentheses
# Time: O(N), Space: O(N) using Stack

def is_valid_parentheses(s: str) -> bool:
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in pairs.values():
            stack.append(char)
        elif char in pairs.keys():
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0

if __name__ == "__main__":
    print(is_valid_parentheses("{[()]}")) # True
    print(is_valid_parentheses("{[(])}")) # False
