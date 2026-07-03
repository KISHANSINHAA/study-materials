# ====================================================================
# THEORY & CONCEPT:
# Character frequency tracks occurrences of each character in a string. This is achieved by mapping each character to its count in a hash map/dictionary, ignoring whitespace.
#
# COMPLEXITY:
# Time Complexity: O(N) to read the string of length N.
# Space Complexity: O(K) where K is the number of unique characters.
#
# INTERVIEW Q&A:
# Q: What Python standard library module is optimal for counting?
# A: The collections.Counter class, which is built specifically for counting hashable objects.
#
# Q: How do you handle spaces or punctuation?
# A: By filtering them out using character checks like `char != ' '` or `char.isalnum()` during iteration.
# ====================================================================

# Python program to calculate character frequency in a string

def char_frequency(s: str) -> dict:
    """
    Calculates frequency of each character in a string (ignoring spaces).
    """
    freq = {}
    for char in s:
        if char != ' ':  # Exclude spaces
            freq[char] = freq.get(char, 0) + 1
    return freq

# Test case
if __name__ == "__main__":
    text = "accenture"
    print(f"Text: {text}")
    print("Character Frequency:", char_frequency(text))
