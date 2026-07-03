# ====================================================================
# THEORY & CONCEPT:
# Classic Data Structure and Algorithm problem. Focuses on spatial optimization, indexing, and temporal efficiencies.
#
# COMPLEXITY:
# Time Complexity: Optimized bound.
# Space Complexity: Minimized auxiliary footprint.
#
# INTERVIEW Q&A:
# Q: What is space-time trade-off?
# A: Designing algorithms to consume more memory (space) to run faster (time), or vice versa.
#
# Q: What is the time complexity of dictionary operations?
# A: Dictionary key insertions, deletions, and lookups take O(1) time on average.
# ====================================================================

# DSA Question: Reverse Linked List
# Time: O(N), Space: O(1) in-place pointer manipulation

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        next_temp = curr.next  # Save next
        curr.next = prev       # Reverse pointer
        prev = curr            # Move prev forward
        curr = next_temp       # Move curr forward
    return prev

def print_list(node: ListNode):
    values = []
    while node:
        values.append(str(node.val))
        node = node.next
    print(" -> ".join(values))

if __name__ == "__main__":
    # Create list: 1 -> 2 -> 3 -> 4
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))
    print("Original List:")
    print_list(head)
    
    reversed_head = reverse_list(head)
    print("Reversed List:")
    print_list(reversed_head)
