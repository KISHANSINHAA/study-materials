# ====================================================================
# THEORY & CONCEPT:
# Power Query (M Language) is the data connection and transformation engine in Power BI.
#
# Core Characteristics of M Language:
# 1. Structure: Formula-based step-by-step structure using `let` and `in`.
#    - `let`: Defines variables/steps representing data states.
#    - `in`: The final step returned to the model.
# 2. Case-sensitivity: M is strictly case-sensitive (`let` is valid, `LET` is a syntax error).
#
# Query Folding:
# - The process where the Power Query engine translates transformation steps (like filtering, joining, groupings)
#   into a single SQL query and pushes it back to the source relational database (SQL Server, Oracle, Snowflake).
# - Importance: Database engines process queries much faster than local Power Query containers. It prevents 
#   loading millions of raw database records into local memory.
# - Blocking Query Folding:
#   - Steps that do not fold: Adding Index Columns, running custom Python/R scripts, merging columns from 
#     different non-foldable sources, and changing datatypes before filtering.
#   - Once a step fails to fold, ALL subsequent steps cannot fold.
# ====================================================================

# M Code Templates for common interview scenarios:
"""
-- 1. Standard Date Calendar Table generation in M
let
    StartDate = #date(2026, 1, 1),
    EndDate = #date(2026, 12, 31),
    DayCount = Duration.Days(Duration.From(EndDate - StartDate)) + 1,
    SourceList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    TableFromList = Table.FromList(SourceList, Splitter.SplitByNothing(), {"Date"}),
    AddedYear = Table.AddColumn(TableFromList, "Year", each Date.Year([Date]), Int64.Type),
    AddedMonth = Table.AddColumn(AddedYear, "Month", each Date.Month([Date]), Int64.Type),
    AddedMonthName = Table.AddColumn(AddedMonth, "MonthName", each Date.MonthName([Date]), type text)
in
    AddedMonthName

-- 2. Conditional Column Example in M
-- Replaces null values in 'Status' with 'Pending'
let
    Source = Sql.Database("server", "db"),
    SalesTable = Source{[Schema="dbo", Item="Sales"]}[Data],
    CleanStatus = Table.AddColumn(SalesTable, "CleanStatus", each if [Status] = null then "Pending" else [Status], type text)
in
    CleanStatus
"""

import pandas as pd

class QueryFoldingSimulator:
    """
    A simulator to illustrate the performance difference between:
    1. Folded query (Transformations compiled to database SQL; fetches only 2 records).
    2. Non-Folded query (Engines fetch all database records locally, then filters in RAM).
    """
    def __init__(self, database_mock_records: list):
        self.db_records = database_mock_records

    def simulate_folded_query(self, target_country: str) -> str:
        """
        Translates M steps into standard SQL. The DB execution runs this SQL 
        directly on the database, scanning/filtering on-disk.
        """
        sql_query = f"SELECT * FROM SalesTable WHERE Country = '{target_country}'"
        print(f"[FOLDED] Generated Native Database SQL: {sql_query}")
        
        # Simulating DB-side execution
        results = [r for r in self.db_records if r["Country"] == target_country]
        print(f"[FOLDED] Transferred only {len(results)} records over the network.")
        return sql_query

    def simulate_non_folded_query(self, target_country: str) -> list:
        """
        If query folding is broken (e.g. by inserting a custom non-folding operation beforehand), 
        Power Query has to fetch ALL database records over the network, loading them into memory, 
        and then filter them locally.
        """
        print("[NON-FOLDED] Query folding broken! Fetching ALL records from database to local memory...")
        # Simulating loading whole table over network
        local_memory_table = self.db_records.copy()
        print(f"[NON-FOLDED] Transferred ALL {len(local_memory_table)} records over the network.")
        
        # Local transformation execution in RAM (simulating local Power Query container)
        filtered_results = [r for r in local_memory_table if r["Country"] == target_country]
        print(f"[NON-FOLDED] Local execution completed. Filtered to {len(filtered_results)} records.")
        return filtered_results


# ====================================================================
# UNIT TEST / VERIFICATION SUITE
# ====================================================================
if __name__ == "__main__":
    import unittest

    class TestPowerQueryM(unittest.TestCase):
        def test_query_folding(self):
            # Database containing 10,000 mock transactions (simulated with 5 items)
            db_data = [
                {"SalesID": 101, "Amount": 100.0, "Country": "USA"},
                {"SalesID": 102, "Amount": 150.0, "Country": "Canada"},
                {"SalesID": 103, "Amount": 200.0, "Country": "USA"},
                {"SalesID": 104, "Amount": 50.0, "Country": "UK"},
                {"SalesID": 105, "Amount": 80.0, "Country": "Canada"}
            ]

            print("\n--- Running Power Query Folding Simulator ---")
            simulator = QueryFoldingSimulator(db_data)

            # Case A: Folded Step (e.g. Filters on Country)
            sql = simulator.simulate_folded_query("Canada")
            self.assertIn("Country = 'Canada'", sql)

            # Case B: Non-folded Step (e.g. custom step before filter forces local retrieval)
            local_results = simulator.simulate_non_folded_query("Canada")
            self.assertEqual(len(local_results), 2)
            print("--- Power Query Simulation Tests Passed ---\n")

    unittest.main(argv=[''], exit=False)
