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

# Python program to add two matrices

def add_matrices(A: list, B: list) -> list:
    """
    Adds two 2D matrices of matching dimensions.
    """
    rows = len(A)
    cols = len(A[0])
    
    # Initialize result matrix with zeros
    result = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            result[i][j] = A[i][j] + B[i][j]
            
    return result

# Test case
if __name__ == "__main__":
    matrix_A = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    matrix_B = [
        [7, 8, 9],
        [1, 2, 3]
    ]
    print("Matrix A:")
    for row in matrix_A: print(row)
    print("Matrix B:")
    for row in matrix_B: print(row)
    
    print("Addition Result:")
    result = add_matrices(matrix_A, matrix_B)
    for row in result: print(row)
