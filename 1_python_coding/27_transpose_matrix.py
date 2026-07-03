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

# Python program to find the transpose of a matrix

def transpose_loops(matrix: list) -> list:
    """
    Transpose using nested loops.
    """
    rows = len(matrix)
    cols = len(matrix[0])
    
    transposed = [[0 for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    return transposed

def transpose_zip(matrix: list) -> list:
    """
    Transpose using zip unpacking (Pythonic).
    """
    return [list(row) for row in zip(*matrix)]

# Test case
if __name__ == "__main__":
    mat = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    print("Original Matrix:")
    for r in mat: print(r)
    
    print("Transposed (Loops):")
    for r in transpose_loops(mat): print(r)
    
    print("Transposed (Zip):")
    for r in transpose_zip(mat): print(r)
