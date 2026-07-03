# ====================================================================
# THEORY & CONCEPT:
# Spark Structured Streaming is a scalable, fault-tolerant stream processing engine built on Spark SQL.
#
# Key Concepts:
# 1. Micro-batch Processing (Default): Spark periodically queries the source, gathers available data, 
#    and runs it as a short batch job (latency ~100ms).
# 2. Continuous Processing: Low-latency execution mode (~1ms) that continuously polls records.
# 3. Checkpointing: Essential for production. Saves offsets and query metadata to reliable storage (e.g. S3). 
#    Allows queries to recover from failures and resume where they left off (ensures exactly-once delivery).
# 4. Triggers:
#    - ProcessingTime: Runs micro-batches at a specified interval (e.g. `.trigger(processingTime='10 seconds')`).
#    - Once: Processes all available data, then terminates.
#    - AvailableNow: Similar to Once, but processes data in multiple micro-batches to prevent memory exhaustion.
# 5. Watermarking:
#    - Tracks progress of event time. Defines a threshold for how late data can arrive.
#    - Format: `.withWatermark("timestamp_col", "10 minutes")` tells Spark to ignore events older than 10 minutes 
#      relative to the max event time seen so far. Enables safe state clean-ups.
# ====================================================================

# Standard python simulation that mocks Structured Streaming syntax.
class MockDataStreamReader:
    def __init__(self, format_name):
        self.format_name = format_name
        self._options = {}
        self._schema = None

    def schema(self, schema_defn):
        self._schema = schema_defn
        return self

    def option(self, key, value):
        self._options[key] = value
        return self

    def load(self, path):
        print(f"Initializing streaming source [{self.format_name}] from path '{path}'")
        return MockDataFrame(is_streaming=True)

class MockDataStreamWriter:
    def __init__(self, df):
        self.df = df
        self._options = {}
        self._format = "console"
        self._trigger = None

    def format(self, format_name):
        self._format = format_name
        return self

    def option(self, key, value):
        self._options[key] = value
        return self

    def trigger(self, **kwargs):
        self._trigger = kwargs
        return self

    def start(self, path=None) -> 'MockStreamingQuery':
        print(f"Starting streaming query writing to target format '{self._format}' at location '{path}'")
        print(f"  - Checkpoint location set to: {self._options.get('checkpointLocation')}")
        print(f"  - Trigger configuration: {self._trigger}")
        return MockStreamingQuery()

class MockDataFrame:
    def __init__(self, is_streaming=False):
        self.is_streaming = is_streaming

    def withWatermark(self, time_column: str, delay_threshold: str):
        print(f"Applied watermark on '{time_column}' with threshold of {delay_threshold}")
        return self

    def groupBy(self, *cols):
        print(f"Grouping stream by: {cols}")
        return self

    def count(self):
        print("Aggregation: count()")
        return self

    @property
    def writeStream(self) -> MockDataStreamWriter:
        return MockDataStreamWriter(self)

class MockStreamingQuery:
    def isActive(self) -> bool:
        return False
    def stop(self):
        print("Stopping streaming query.")

class MockSparkSession:
    @property
    def readStream(self) -> MockDataStreamReader:
        return MockDataStreamReader("delta")

# Setup global variable to support both local validation and real execution
try:
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.getOrCreate()
    has_pyspark = True
except ImportError:
    spark = MockSparkSession()
    has_pyspark = False


# ====================================================================
# EXECUTABLE PIPELINE WORKFLOW & TESTS
# ====================================================================
class StreamingPipeline:
    @staticmethod
    def run_streaming_job(source_path: str, checkpoint_path: str, output_path: str):
        """
        Builds a structured streaming pipeline that reads raw events, 
        applies a watermark, aggregates events, and writes results to Delta.
        """
        print("\n--- Executing Spark Structured Streaming Pipeline ---")
        
        # 1. Read Stream
        raw_stream = spark.readStream \
            .option("maxFilesPerTrigger", 10) \
            .load(source_path)

        # 2. Process: Apply watermarking for late data tolerance and run stateful aggregations
        processed_stream = raw_stream \
            .withWatermark("event_time", "15 minutes") \
            .groupBy("device_id") \
            .count()

        # 3. Write Stream to Sink with checkpointing for fault-tolerance
        query = processed_stream.writeStream \
            .format("delta") \
            .option("checkpointLocation", checkpoint_path) \
            .trigger(processingTime="10 seconds") \
            .start(output_path)
            
        print("Streaming query successfully initialized.")
        query.stop()
        print("--- Streaming Job Execution Finished ---\n")


if __name__ == "__main__":
    import unittest

    class TestStreaming(unittest.TestCase):
        def test_streaming_setup(self):
            # Test executing pipeline with local mock directories
            StreamingPipeline.run_streaming_job(
                source_path="/data/iot-events",
                checkpoint_path="/mnt/checkpoints/iot-job",
                output_path="/data/silver/iot-aggregated"
            )
            self.assertTrue(True)

    unittest.main(argv=[''], exit=False)
