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

# Python program to reverse words in a sentence
# Example: "hello world" -> "world hello"

def reverse_words(s: str) -> str:
    """
    Reverses the order of words in a sentence.
    """
    words = s.split()
    reversed_words = words[::-1]
    return " ".join(reversed_words)

# Test case
if __name__ == "__main__":
    sentence = "Python is a powerful programming language"
    print("Original:", sentence)
    print("Reversed:", reverse_words(sentence))
