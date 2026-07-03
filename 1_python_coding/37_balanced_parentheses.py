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

# Python program to check for Balanced Parentheses
# Using stack data structure. Time Complexity: O(N).

def is_balanced(expression: str) -> bool:
    """
    Checks if braces (), [], {} are balanced in expression.
    """
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in expression:
        if char in mapping.values():  # If it is an opening brace
            stack.append(char)
        elif char in mapping.keys():  # If it is a closing brace
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
            
    return len(stack) == 0

# Test cases
if __name__ == "__main__":
    test_exprs = [
        "{[()]}",
        "{[(])}",
        "((()))",
        "()[]{}",
        "({)}"
    ]
    for expr in test_exprs:
        print(f"Expression: {expr:10} -> Balanced? {is_balanced(expr)}")
