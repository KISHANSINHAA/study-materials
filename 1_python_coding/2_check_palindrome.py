# ====================================================================
# THEORY & CONCEPT:
# A palindrome is a sequence that reads the same backward as forward. The optimal check cleans the string of spaces and punctuation, then uses two pointers meeting at the center to check symmetry in O(1) auxiliary space.
#
# COMPLEXITY:
# Time Complexity: O(N) to clean and traverse the string.
# Space Complexity: O(N) for clean copy (or O(1) if checked in-place).
#
# INTERVIEW Q&A:
# Q: What is the advantage of the two-pointer approach?
# A: It allows in-place checking without allocating memory for a reversed copy of the string, optimizing space to O(1).
#
# Q: How does code handle case insensitivity?
# A: By converting characters to lowercase or uppercase using `.lower()` or `.upper()` during comparison.
# ====================================================================

# Python program to check if a string is a palindrome
# A palindrome reads the same backward as forward.

def is_palindrome(s: str) -> bool:
    """
    Checks if the string is a palindrome.
    We convert the string to lowercase and remove non-alphanumeric characters
    to handle spaces, punctuation, and case sensitivity.
    """
    # Clean the string (keep only alphanumeric characters)
    cleaned = "".join(char.lower() for char in s if char.isalnum())
    
    # Compare the cleaned string with its reverse
    return cleaned == cleaned[::-1]

# Test cases
if __name__ == "__main__":
    test_cases = [
        "radar",
        "A man, a plan, a canal: Panama",
        "hello",
        "12321",
        "Accenture"
    ]
    
    for case in test_cases:
        print(f"Is '{case}' a palindrome? -> {is_palindrome(case)}")
