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

# Python program to check if two strings are anagrams
# Two strings are anagrams if they contain the same characters in the same frequency.

def is_anagram_sorted(s1: str, s2: str) -> bool:
    """
    Sorts both strings and compares.
    Time Complexity: O(N log N).
    """
    # Clean inputs: remove spaces and convert to lowercase
    c1 = "".join(s1.split()).lower()
    c2 = "".join(s2.split()).lower()
    return sorted(c1) == sorted(c2)

def is_anagram_dict(s1: str, s2: str) -> bool:
    """
    Counts character frequencies using a dictionary.
    Time Complexity: O(N).
    """
    c1 = "".join(s1.split()).lower()
    c2 = "".join(s2.split()).lower()
    
    if len(c1) != len(c2):
        return False
        
    freq = {}
    for char in c1:
        freq[char] = freq.get(char, 0) + 1
        
    for char in c2:
        if char not in freq:
            return False
        freq[char] -= 1
        if freq[char] < 0:
            return False
            
    return True

# Test cases
if __name__ == "__main__":
    str1, str2 = "listen", "silent"
    print(f"Are '{str1}' and '{str2}' anagrams? (Sorted method) -> {is_anagram_sorted(str1, str2)}")
    print(f"Are '{str1}' and '{str2}' anagrams? (Dict method)   -> {is_anagram_dict(str1, str2)}")
