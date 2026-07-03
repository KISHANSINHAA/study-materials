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

# Python program to count words in a string

def count_words(s: str) -> int:
    """
    Splits string by whitespace and returns count of elements.
    """
    if not s.strip():
        return 0
    return len(s.split())

# Test case
if __name__ == "__main__":
    text = "  Hello  World! Python programming   is fun.  "
    print(f"Text: '{text}'")
    print("Word Count:", count_words(text))
