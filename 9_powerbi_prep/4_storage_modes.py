# ====================================================================
# THEORY & CONCEPT:
# Storage Modes define how data is stored and queried in a Power BI report.
#
# Core Storage Modes:
# 1. Import Mode (Default):
#    - Loads the entire dataset into Power BI memory (RAM).
#    - Highly compressed using the VertiPaq engine.
#    - Delivers single-digit millisecond query performance.
#    - Requires scheduled refresh to display updated data.
# 2. DirectQuery Mode:
#    - Data remains in the source database. Power BI sends real-time SQL queries to the source at runtime.
#    - Useful for real-time reporting or datasets too large to fit in memory (10GB+).
#    - Drawback: Performance depends on the source DB, and DAX functions are restricted.
# 3. Live Connection:
#    - Connects directly to an external Analysis Services model (SSAS, Azure AS, or Power BI dataset).
#    - No modeling or transformations allowed; calculations reside entirely in the host database.
# 4. Composite Model (Dual Mode):
#    - Combines Import and DirectQuery tables in a single model.
#    - Tables set to "Dual" act as Import when joined with Import tables, and as DirectQuery when joined with DirectQuery.
#
# The VertiPaq Compression Engine:
# An in-memory, columnar engine. It achieves high compression using:
# 1. Value Encoding: Math-based reduction (e.g. storing value shifts to fit data into smaller bit-sizes).
# 2. Dictionary Encoding: Replaces text values with integer keys.
# 3. Run-Length Encoding (RLE): Compresses repeating values in a sorted column.
#    Instead of storing "A, A, A, B, B", it stores "A: 3 times, B: 2 times".
# ====================================================================

class VertiPaqCompressor:
    """
    Simulates how the Power BI VertiPaq engine performs Dictionary Encoding 
    and Run-Length Encoding (RLE) to achieve extreme columnar compression.
    """
    @staticmethod
    def compress_column(column_data: list) -> dict:
        # 1. Dictionary Encoding (Mapping unique items to integer IDs)
        unique_values = sorted(list(set(column_data)))
        value_to_id = {val: idx for idx, val in enumerate(unique_values)}
        id_to_value = {idx: val for idx, val in enumerate(unique_values)}
        
        encoded_ids = [value_to_id[item] for item in column_data]

        # 2. Run-Length Encoding (RLE) on the IDs
        # Compresses repeating sequence of IDs: e.g. [0, 0, 0, 1, 1] -> [(0, 3), (1, 2)]
        rle_compressed = []
        if not encoded_ids:
            return {"dictionary": id_to_value, "rle": []}

        current_id = encoded_ids[0]
        current_count = 1

        for item_id in encoded_ids[1:]:
            if item_id == current_id:
                current_count += 1
            else:
                rle_compressed.append((current_id, current_count))
                current_id = item_id
                current_count = 1
        rle_compressed.append((current_id, current_count)) # Append final group

        return {
            "dictionary": id_to_value,
            "rle": rle_compressed,
            "original_count": len(column_data),
            "compressed_count": len(rle_compressed)
        }


# ====================================================================
# UNIT TEST / VERIFICATION SUITE
# ====================================================================
if __name__ == "__main__":
    import unittest

    class TestStorageModesAndCompression(unittest.TestCase):
        def test_vertipaq_simulation(self):
            # Column containing repeating values (e.g. Sales Territory Country)
            # Sorting columns makes repeating blocks contiguous, optimizing RLE!
            countries_column = sorted([
                "USA", "USA", "USA", "USA", "USA",
                "Canada", "Canada", "Canada",
                "UK", "UK", "UK", "UK",
                "Germany", "Germany"
            ])

            print("\n--- Running VertiPaq Compression Simulation ---")
            print("Original Column Row Count:", len(countries_column))

            # Run VertiPaq compression
            result = VertiPaqCompressor.compress_column(countries_column)
            
            print("Dictionary Map (ID -> Value):")
            for item_id, val in result["dictionary"].items():
                print(f"  {item_id}: {val}")

            print("Run-Length Encoded (RLE) Streams:")
            print("  Format: (Value_ID, Repeat_Count)")
            for item in result["rle"]:
                print(f"  {item}")

            # Original size was 14 rows. Compressed size is 4 groups.
            self.assertEqual(result["original_count"], 14)
            self.assertEqual(result["compressed_count"], 4)
            self.assertEqual(result["rle"][0], (0, 3)) # Canada (ID 0) repeats 3 times
            print(f"Compression Ratio (Rows vs RLE Blocks): {result['original_count']} : {result['compressed_count']}")
            print("--- VertiPaq Compressor Tests Passed Successfully ---\n")

    unittest.main(argv=[''], exit=False)
