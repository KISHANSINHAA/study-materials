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

# Python program to find the largest element in a list

def find_largest(arr: list):
    """
    Returns the maximum element in a list.
    """
    if not arr:
        return None
        
    # Python built-in method
    builtin_max = max(arr)
    
    # Manual loop method
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
            
    return max_val

# Test case
if __name__ == "__main__":
    nums = [12, 45, 2, 89, 34, 11]
    print(f"List: {nums}")
    print(f"Largest element: {find_largest(nums)}")
