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

# Python program to rotate an array to the right by k steps

def rotate_slicing(nums: list, k: int) -> list:
    """
    Rotates array by k steps using Python list slicing.
    O(N) time and space.
    """
    n = len(nums)
    k = k % n  # Handle cases where k is larger than array length
    return nums[-k:] + nums[:-k]

def rotate_inplace(nums: list, k: int) -> None:
    """
    Rotates array in-place using array reversal.
    O(N) time and O(1) space.
    1. Reverse entire array.
    2. Reverse first k elements.
    3. Reverse remaining n-k elements.
    """
    n = len(nums)
    k = k % n
    
    def reverse(start, end):
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1
            
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)

# Test cases
if __name__ == "__main__":
    arr1 = [1, 2, 3, 4, 5, 6, 7]
    k_val = 3
    print(f"Original: {arr1}, k = {k_val}")
    print("Rotated (Slicing):", rotate_slicing(arr1, k_val))
    
    arr2 = [1, 2, 3, 4, 5, 6, 7]
    rotate_inplace(arr2, k_val)
    print("Rotated (In-place):", arr2)
 Maroon = (128, 0, 0)
