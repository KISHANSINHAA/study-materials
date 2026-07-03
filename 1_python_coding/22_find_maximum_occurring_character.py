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

# Python program to find the maximum occurring character in a string

def max_occurring_char(s: str) -> tuple:
    """
    Returns the character with highest frequency and its count.
    """
    if not s:
        return None, 0
        
    freq = {}
    for char in s:
        if char != ' ':
            freq[char] = freq.get(char, 0) + 1
            
    # Find key with maximum value
    max_char = max(freq, key=freq.get)
    return max_char, freq[max_char]

# Test case
if __name__ == "__main__":
    text = "success is sweetest when you achieve it"
    char, count = max_occurring_char(text)
    print(f"Text: '{text}'")
    print(f"Max Occurring Character: '{char}' (Occurred {count} times)")
