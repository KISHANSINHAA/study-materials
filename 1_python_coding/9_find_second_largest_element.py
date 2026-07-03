# ====================================================================
# THEORY & CONCEPT:
# Finding the second largest element in a list in a single pass. We maintain two variables: 'largest' and 'second_largest'. During iteration, we update these variables depending on whether the current element is greater than 'largest' or between 'second_largest' and 'largest'.
#
# COMPLEXITY:
# Time Complexity: O(N) as we check each element exactly once.
# Space Complexity: O(1) auxiliary space.
#
# INTERVIEW Q&A:
# Q: Can you find the second largest by sorting?
# A: Yes, by sorting in descending order and finding the second unique element. However, sorting takes O(N log N) which is slower than a single O(N) pass.
#
# Q: How do you handle duplicate values?
# A: By ensuring that 'second_largest' is only updated with values strictly less than 'largest' (num != largest).
# ====================================================================

# Python program to find the second largest element in a list
# Crucial requirement: Must handle duplicates and run in O(N) time with O(1) auxiliary space.

def find_second_largest(arr: list):
    """
    Finds the second largest element in a single pass.
    Returns None if the list has fewer than 2 unique elements.
    """
    if len(arr) < 2:
        return None
        
    largest = float('-inf')
    second_largest = float('-inf')
    
    for num in arr:
        if num > largest:
            second_largest = largest
            largest = num
        elif num > second_largest and num != largest:
            second_largest = num
            
    return second_largest if second_largest != float('-inf') else None

# Test cases
if __name__ == "__main__":
    test_lists = [
        [12, 35, 1, 10, 34, 1],
        [10, 10, 10],
        [10, 5],
        [5, 10],
        [1, 2, 3, 4, 5]
    ]
    for lst in test_lists:
        print(f"List: {lst} -> Second Largest: {find_second_largest(lst)}")
