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

# Python program to merge two lists

def merge_plus_operator(l1: list, l2: list) -> list:
    return l1 + l2

def merge_unpacking(l1: list, l2: list) -> list:
    return [*l1, *l2]

def merge_extend(l1: list, l2: list) -> list:
    # Note: modifies the first list in place
    temp = l1.copy()
    temp.extend(l2)
    return temp

# Test cases
if __name__ == "__main__":
    list_a = [1, 2, 3]
    list_b = [4, 5, 6]
    print("List A:", list_a)
    print("List B:", list_b)
    print("Merged (+ operator):", merge_plus_operator(list_a, list_b))
    print("Merged (Unpacking):  ", merge_unpacking(list_a, list_b))
    print("Merged (Extend):     ", merge_extend(list_a, list_b))
