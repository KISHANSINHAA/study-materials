# ====================================================================
# THEORY & CONCEPT:
# DAX (Data Analysis Expressions) is the formula language used in Power BI for data modeling and calculations.
#
# Two Core Contexts in DAX:
# 1. Row Context:
#    - Represents the "current row" scan.
#    - Exists naturally inside Calculated Columns and Iterators (e.g. SUMX, FILTER, AVERAGEX).
#    - Does not cross relationships between tables automatically (requires RELATED or RELATEDTABLE).
# 2. Filter Context:
#    - The set of active filters applied to the data model by visuals, slicers, page filters, or DAX formulas.
#    - Exists dynamically at visual rendering time.
#
# Context Transition:
# - The process where a Row Context is converted into a Filter Context.
# - Occurs exclusively when you call `CALCULATE` (or a Measure, which contains an implicit `CALCULATE`) 
#   inside a Row Context (e.g., inside a calculated column or an iterator).
#
# Measures vs Calculated Columns:
# - Calculated Columns: Calculated row-by-row during data refresh. Stored in RAM, increasing model file size.
# - Measures: Evaluated dynamically on the fly at visual rendering time. Consumes CPU, but uses 0 static memory.
#
# CALCULATE Function:
# - Syntax: CALCULATE(<expression>, <filter1>, <filter2>, ...)
# - It is the only function in DAX that can modify the Filter Context (e.g. overriding, appending, or removing filters).
# ====================================================================

# DAX Code Templates for common interview scenarios:
"""
-- 1. Simple Measure
Total_Sales = SUM(Sales[Revenue])

-- 2. CALCULATE overriding a filter (Calculating USA Sales regardless of visual slicers)
US_Sales = CALCULATE([Total_Sales], Customers[Country] = "USA")

-- 3. Time Intelligence (Year-to-Date Sales)
YTD_Sales = TOTALYTD([Total_Sales], 'Calendar'[Date])

-- 4. Prior Year Sales (Comparison)
Sales_Prior_Year = CALCULATE([Total_Sales], SAMEPERIODLASTYEAR('Calendar'[Date]))

-- 5. Context Transition Example in a Calculated Column
-- (This counts how many transactions that customer has done by transforming the customer row into a filter context)
Customer_Tx_Count = CALCULATE(COUNT(Sales[SalesID]))
"""

import pandas as pd

class DAXSimulator:
    """
    A Python engine using Pandas that simulates how the DAX engine evaluates Row Context and Filter Context.
    """
    def __init__(self, sales_df: pd.DataFrame):
        self.sales = sales_df
        # Default global filter context (no filters applied)
        self.global_filter_context = {}

    def calculate(self, expression_func, *filter_funcs) -> float:
        """
        Simulates the DAX CALCULATE function.
        Evaluates the expression_func in a MODIFIED filter context defined by filter_funcs.
        """
        # Apply filters to table to form the new filter context
        filtered_df = self.sales.copy()
        for filter_func in filter_funcs:
            filtered_df = filter_func(filtered_df)
            
        # Evaluate expression in this new filter context
        return expression_func(filtered_df)

    def sum_sales_revenue(self, df: pd.DataFrame) -> float:
        """Simulates: SUM(Sales[Revenue])"""
        if df.empty:
            return 0.0
        return df["revenue"].sum()

    def sumx_net_revenue(self, df: pd.DataFrame, tax_rate: float) -> float:
        """
        Simulates: SUMX(Sales, Sales[Revenue] * (1 - tax_rate))
        SUMX is an iterator: it creates a Row Context and evaluates the expression row-by-row, then sums.
        """
        total = 0.0
        # Row Context loop
        for index, row in df.iterrows():
            row_revenue = row["revenue"]
            row_net = row_revenue * (1 - tax_rate) # Row Context evaluation
            total += row_net
        return total


# ====================================================================
# UNIT TEST / VERIFICATION SUITE
# ====================================================================
if __name__ == "__main__":
    import unittest

    class TestDAXFundamentals(unittest.TestCase):
        def setUp(self):
            # Setup sample transactions table
            data = {
                "transaction_id": [1, 2, 3, 4, 5],
                "country": ["USA", "Canada", "USA", "UK", "Canada"],
                "category": ["Electronics", "Books", "Electronics", "Electronics", "Books"],
                "revenue": [100.0, 50.0, 200.0, 150.0, 30.0]
            }
            self.sales_df = pd.DataFrame(data)
            self.dax = DAXSimulator(self.sales_df)

        def test_calculate_sales(self):
            print("\n--- Running DAX Simulator Tests ---")
            
            # Test 1: Simple SUM
            total_sales = self.dax.calculate(self.dax.sum_sales_revenue)
            self.assertEqual(total_sales, 530.0)
            print(f"DAX Simulation: [Total_Sales] = {total_sales}")

            # Test 2: CALCULATE US Sales (Overriding Filter Context)
            def filter_usa(df):
                return df[df["country"] == "USA"]

            us_sales = self.dax.calculate(self.dax.sum_sales_revenue, filter_usa)
            self.assertEqual(us_sales, 300.0)
            print(f"DAX Simulation: [US_Sales] = {us_sales}")

            # Test 3: CALCULATE US Electronics Sales (Multiple Filters)
            def filter_electronics(df):
                return df[df["category"] == "Electronics"]

            us_elec_sales = self.dax.calculate(self.dax.sum_sales_revenue, filter_usa, filter_electronics)
            self.assertEqual(us_elec_sales, 300.0) # both USA transactions are electronics
            print(f"DAX Simulation: [US_Electronics_Sales] = {us_elec_sales}")

            # Test 4: SUMX (Iterator) with 10% tax rate
            net_sales = self.dax.sumx_net_revenue(self.sales_df, tax_rate=0.10)
            self.assertAlmostEqual(net_sales, 477.0)
            print(f"DAX Simulation: SUMX Net Sales (10% Tax) = {net_sales}")
            print("--- DAX Simulator Tests Passed Successfully ---\n")

    unittest.main(argv=[''], exit=False)
