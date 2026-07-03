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

# Python program to move all zeros in an array to the end
# Constraint: Must be in-place, preserving order of non-zero elements.

def move_zeros(nums: list) -> None:
    """
    Moves zeros to the end in O(N) time and O(1) space.
    """
    insert_pos = 0
    # Copy non-zero elements forward
    for num in nums:
        if num != 0:
            nums[insert_pos] = num
            insert_pos += 1
            
    # Fill remainder of list with zeros
    for i in range(insert_pos, len(nums)):
        nums[i] = 0

# Test case
if __name__ == "__main__":
    arr = [0, 1, 0, 3, 12]
    print("Original:", arr)
    move_zeros(arr)
    print("Result:  ", arr)
