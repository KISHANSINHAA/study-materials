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

# Python program to count frequency of elements in a list

from collections import Counter

def count_frequency_dict(arr: list) -> dict:
    """
    Counts frequency using a standard dictionary.
    """
    freq = {}
    for item in arr:
        freq[item] = freq.get(item, 0) + 1
    return freq

def count_frequency_counter(arr: list) -> Counter:
    """
    Counts frequency using built-in collections.Counter.
    """
    return Counter(arr)

# Test cases
if __name__ == "__main__":
    data = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
    print("Input List:", data)
    print("Frequency (Standard Dict):", count_frequency_dict(data))
    print("Frequency (Counter):", dict(count_frequency_counter(data)))
