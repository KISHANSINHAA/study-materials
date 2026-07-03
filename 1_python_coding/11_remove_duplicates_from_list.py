# ====================================================================
# THEORY & CONCEPT:
# Duplicates can be removed by converting a list to a set because set elements are unique and hash-lookup takes O(1) time. However, sets do not preserve element insertion order. Preserving order requires using dictionaries (`dict.fromkeys()`).
#
# COMPLEXITY:
# Time Complexity: O(N) to traverse the list and insert into the set/dictionary.
# Space Complexity: O(N) to store unique elements.
#
# INTERVIEW Q&A:
# Q: How do you remove duplicates while preserving list order?
# A: By using list(dict.fromkeys(array)) in Python 3.7+, which guarantees insertion order preservation.
#
# Q: Why is set conversion faster than nested loops?
# A: Set lookup/insertion is O(1) on average due to hashing, whereas nested loops require O(N^2) comparison time.
# ====================================================================

# Python program to remove duplicates from a list

def remove_duplicates_unordered(arr: list) -> list:
    """
    Removes duplicates by converting to set.
    Note: Does NOT preserve order.
    """
    return list(set(arr))

def remove_duplicates_preserve_order(arr: list) -> list:
    """
    Removes duplicates while preserving the original order.
    Using dict.fromkeys() which keeps keys in insertion order.
    """
    return list(dict.fromkeys(arr))

# Test cases
if __name__ == "__main__":
    original = [1, 2, 3, 2, 4, 1, 5, 3]
    print("Original List:", original)
    print("Unordered (Set method):", remove_duplicates_unordered(original))
    print("Ordered (Dict method): ", remove_duplicates_preserve_order(original))
