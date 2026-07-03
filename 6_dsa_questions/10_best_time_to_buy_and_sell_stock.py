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

# DSA Question: Best Time to Buy and Sell Stock
# Time: O(N), Space: O(1)

def max_profit(prices: list) -> int:
    min_price = float('inf')
    max_prof = 0
    
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_prof:
            max_prof = price - min_price
            
    return max_prof

if __name__ == "__main__":
    print(max_profit([7, 1, 5, 3, 6, 4])) # 5 (buy at 1, sell at 6)
