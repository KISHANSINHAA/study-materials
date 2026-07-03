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

# Python program to multiply two matrices
# Dimension compatibility check: A is m x n, B is n x p -> Result is m x p.

def multiply_matrices(A: list, B: list) -> list:
    """
    Multiplies two matrices A and B.
    """
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("Matrices dimensions are incompatible for multiplication.")
        
    # Initialize result matrix with zeros (dimensions rows_A x cols_B)
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            # Dot product of row i of A and col j of B
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(cols_A))
            
    return result

# Test case
if __name__ == "__main__":
    matrix_A = [
        [1, 2],
        [3, 4]
    ]
    matrix_B = [
        [5, 6],
        [7, 8]
    ]
    print("Matrix A:")
    for r in matrix_A: print(r)
    print("Matrix B:")
    for r in matrix_B: print(r)
    
    print("Multiplication Result:")
    result = multiply_matrices(matrix_A, matrix_B)
    for r in result: print(r)
