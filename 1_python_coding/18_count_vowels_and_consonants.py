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

# Python program to count vowels and consonants in a string

def count_vowels_consonants(s: str):
    """
    Counts the number of vowels and consonants in a string.
    """
    vowels_set = set("aeiouAEIOU")
    vowels_count = 0
    consonants_count = 0
    
    for char in s:
        if char.isalpha():
            if char in vowels_set:
                vowels_count += 1
            else:
                consonants_count += 1
                
    return vowels_count, consonants_count

# Test case
if __name__ == "__main__":
    text = "Accenture Careers India 2026"
    v, c = count_vowels_consonants(text)
    print("Text:", text)
    print("Vowels:", v)
    print("Consonants:", c)
