# ====================================================================
# THEORY & CONCEPT:
# Data Modeling is the foundation of Power BI. A good model ensures fast DAX query speeds and accurate results.
#
# Star Schema (Best Practice):
# - Central Fact Table (contains numeric metrics/keys: Sales, Revenue, Quantities).
# - Surrounded by Dimension Tables (contains descriptive attributes: Customer name, Products, Geography, Date).
# - Relationships should be 1-to-Many (1:*) flowing from Dimension (1) to Fact (*).
#
# Snowflake Schema:
# - Normalizes dimensions (e.g., Products table links to Sub-category, which links to Category).
# - Discouraged in Power BI: increases query execution joins, reduces compression efficiency, and slows visual rendering.
#
# Cross Filter Direction:
# - Single (Default): Filters flow from the 1-side of the relationship to the Many-side. (e.g., filtering Customer filters Sales).
# - Both (Bidirectional): Filters flow in both directions. 
#   - Dangers: Severe performance drop, ambiguous relationships, and circular reference bugs. Avoid unless absolutely necessary.
#
# Active vs Inactive Relationships:
# - Only one relationship path can be active between two tables. 
# - Inactive relationships can be activated programmatically in DAX calculations using `USERELATIONSHIP()`.
#   Example: Prior Year Sales based on Shipping Date instead of default Order Date.
# ====================================================================

# DAX Code Templates for modeling scenarios:
"""
-- Activating an Inactive Relationship in DAX
Sales_By_Ship_Date = 
CALCULATE(
    [Total_Sales],
    USERELATIONSHIP(Sales[ShipDate], 'Calendar'[Date])
)
"""

import pandas as pd

class ModelSimulator:
    """
    Simulates how Power BI propagates filter contexts through active/inactive 
    and single/bidirectional relationships.
    """
    def __init__(self):
        # 1. Fact Table (Sales)
        self.sales = pd.DataFrame({
            "sales_id": [1, 2, 3, 4],
            "customer_id": [101, 102, 101, 103],
            "order_date": ["2026-07-01", "2026-07-01", "2026-07-02", "2026-07-02"],
            "ship_date": ["2026-07-03", "2026-07-02", "2026-07-03", "2026-07-05"],
            "revenue": [100.0, 200.0, 150.0, 50.0]
        })

        # 2. Customer Dimension (1-side)
        self.customers = pd.DataFrame({
            "customer_id": [101, 102, 103],
            "customer_name": ["Alice", "Bob", "Charlie"],
            "region": ["East", "West", "East"]
        })

        # 3. Calendar Dimension
        self.calendar = pd.DataFrame({
            "date": ["2026-07-01", "2026-07-02", "2026-07-03", "2026-07-04", "2026-07-05"]
        })

    def filter_dimension_to_fact_single(self, region_filter: str) -> pd.DataFrame:
        """
        Simulates SINGLE filter direction: Dimension -> Fact.
        Filtering customers in 'East' filters the Sales table.
        """
        # Get active customer IDs in the filtered region
        active_customers = self.customers[self.customers["region"] == region_filter]["customer_id"]
        # Propagation: filter sales where customer_id matches
        filtered_sales = self.sales[self.sales["customer_id"].isin(active_customers)]
        return filtered_sales

    def simulate_userelationship(self, calendar_date: str, use_ship_date: bool = False) -> pd.DataFrame:
        """
        Simulates Active vs Inactive relationships.
        Default active relationship is Calendar[date] -> Sales[order_date].
        Inactive relationship (activated by USERELATIONSHIP) is Calendar[date] -> Sales[ship_date].
        """
        if use_ship_date:
            # Activate inactive relationship (ship_date)
            return self.sales[self.sales["ship_date"] == calendar_date]
        else:
            # Use active relationship (order_date)
            return self.sales[self.sales["order_date"] == calendar_date]


# ====================================================================
# UNIT TEST / VERIFICATION SUITE
# ====================================================================
if __name__ == "__main__":
    import unittest

    class TestDataModeling(unittest.TestCase):
        def setUp(self):
            self.model = ModelSimulator()

        def test_single_filter_propagation(self):
            print("\n--- Running Data Modeling Filter Propagation Tests ---")
            
            # Filter Customer Region = 'East'
            # Should propagate to Sales and return Alice (Sales IDs 1, 3) and Charlie (Sales ID 4)
            filtered_sales = self.model.filter_dimension_to_fact_single("East")
            self.assertEqual(len(filtered_sales), 3)
            self.assertEqual(filtered_sales["revenue"].sum(), 300.0)
            print("Filtered Sales Revenue for Region 'East':", filtered_sales["revenue"].sum())

        def test_inactive_relationship_activation(self):
            # Test default relationship on '2026-07-02' (Order date)
            # Sales ID 3 (Order 2026-07-02), Sales ID 4 (Order 2026-07-02) -> Total 200.0
            default_sales = self.model.simulate_userelationship("2026-07-02", use_ship_date=False)
            self.assertEqual(len(default_sales), 2)
            self.assertEqual(default_sales["revenue"].sum(), 200.0)
            print("Default relationship (Order Date) sales count:", len(default_sales))

            # Test USERELATIONSHIP ship_date on '2026-07-02' (Ship date)
            # Sales ID 2 (Shipped 2026-07-02) -> Total 200.0
            ship_date_sales = self.model.simulate_userelationship("2026-07-02", use_ship_date=True)
            self.assertEqual(len(ship_date_sales), 1)
            self.assertEqual(ship_date_sales["revenue"].sum(), 200.0)
            print("USERELATIONSHIP active (Ship Date) sales count:", len(ship_date_sales))
            print("--- Data Modeling Tests Passed Successfully ---\n")

    unittest.main(argv=[''], exit=False)
