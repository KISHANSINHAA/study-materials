# ====================================================================
# THEORY & CONCEPT:
# Databricks Utilities (DBUtils) is a suite of built-in APIs to perform workspace, file system, 
# and secrets management inside Databricks environments.
#
# Core Modules:
# 1. dbutils.fs (File System):
#    - Interacts with DBFS (Databricks File System), which is an abstraction layer over S3/ADLS.
#    - Allows standard operations: listing (ls), copying (cp), moving (mv), creating directories (mkdirs), 
#      and mounting cloud storage (mount).
# 2. dbutils.secrets (Secrets Utility):
#    - Retrieves keys and credentials securely without exposing them in notebooks.
#    - Scopes: Secrets are organized into logical groupings called "scopes" (backed by Databricks KMS or Azure Key Vault).
#    - Redaction: Databricks automatically redacts secret values in notebook outputs, replacing them with `[REDACTED]`.
# 3. dbutils.widgets (Widgets Utility):
#    - Implements parameters that users can change at runtime from the notebook UI.
#    - Widgets can be dropdowns, text inputs, combo boxes, or multi-select lists.
#
# INTERVIEW Q&A:
# Q: Why is mounting storage with dbutils.fs.mount discouraged in modern Databricks architectures?
# A: Mounts are workspace-scoped and accessible by anyone with access to that workspace, presenting security risks. 
#    The modern practice is to use Databricks Unity Catalog, which manages access at the catalog/schema/table/file level 
#    via Storage Credentials and External Locations.
#
# Q: How does Databricks handle credentials in notebooks? Explain Secret Scopes.
# A: Secret scopes house key-value pairs securely. In Python, you fetch credentials using 
#    `password = dbutils.secrets.get(scope="my_scope", key="my_key")`. 
#    Even if you print `password`, the notebook output will show `[REDACTED]` to prevent leakages.
# ====================================================================

# Standard structure to support local mock execution while matching real Databricks API calls.
class DBUtilsFS:
    def __init__(self):
        self.mounts = {}

    def ls(self, path: str) -> list:
        print(f"Listing contents of DBFS path: {path}")
        return [{"path": f"{path}/file1.csv", "name": "file1.csv", "size": 1024}]

    def cp(self, source: str, destination: str, recurse: bool = False) -> bool:
        print(f"Copying {source} to {destination} (Recurse={recurse})")
        return True

    def mount(self, source: str, mount_point: str, extra_configs: dict = None) -> bool:
        print(f"Mounting bucket '{source}' to local mount point '{mount_point}'")
        self.mounts[mount_point] = {
            "source": source,
            "extra_configs": extra_configs or {}
        }
        return True

    def mounts(self) -> dict:
        return self.mounts

class DBUtilsSecrets:
    def __init__(self):
        self._secrets_store = {
            "dw-credentials-scope": {
                "dw_password": "super_secure_dw_pass_123",
                "dw_user": "analyst_prod"
            }
        }

    def get(self, scope: str, key: str) -> str:
        """
        Retrieves a secret. Implements Databricks output redaction standard.
        """
        if scope in self._secrets_store and key in self._secrets_store[scope]:
            real_value = self._secrets_store[scope][key]
            # Redacted representation returned when printing, but internally returns the value
            class RedactedString(str):
                def __repr__(self):
                    return "[REDACTED]"
                def __str__(self):
                    return "[REDACTED]"
                def get_raw(self):
                    return real_value
            return RedactedString(real_value)
        else:
            raise Exception(f"Secret key '{key}' in scope '{scope}' not found.")

class DBUtilsWidgets:
    def __init__(self):
        self.widgets = {}

    def text(self, name: str, default: str, label: str = None):
        self.widgets[name] = default

    def get(self, name: str) -> str:
        return self.widgets.get(name, "")

class MockDBUtils:
    def __init__(self):
        self.fs = DBUtilsFS()
        self.secrets = DBUtilsSecrets()
        self.widgets = DBUtilsWidgets()

# In Databricks, the `dbutils` object is globally available. 
# We declare it or use the mock locally.
try:
    # If in Databricks environment, retrieve the real global dbutils
    import IPython
    dbutils = IPython.get_ipython().user_ns["dbutils"]
except (ImportError, AttributeError, KeyError):
    # Local fallback
    dbutils = MockDBUtils()


# ====================================================================
# EXECUTABLE PRODUCTION WORKFLOW & TESTS
# ====================================================================
class DatabricksWorkflow:
    @staticmethod
    def run_pipeline():
        """
        Simulates standard ETL initialization steps in a Databricks Notebook.
        """
        print("\n--- Starting Databricks Notebook Workflow Simulation ---")
        
        # 1. Setup Input Widgets (e.g. dynamic date parameters)
        dbutils.widgets.text("run_date", "2026-07-02", "Job Execution Date")
        run_date = dbutils.widgets.get("run_date")
        print(f"Widget retrieved run_date: {run_date}")

        # 2. Retrieve secure credentials from scope
        db_user = dbutils.secrets.get(scope="dw-credentials-scope", key="dw_user")
        db_pass = dbutils.secrets.get(scope="dw-credentials-scope", key="dw_password")
        
        # Verify redaction logic works (printing yields [REDACTED])
        print(f"Connecting to database with User: '{db_user}' and Password: '{db_pass}'")
        
        # 3. Mount external cloud storage
        dbutils.fs.mount(
            source="s3a://my-enterprise-data-lake-raw",
            mount_point="/mnt/raw_data",
            extra_configs={"fs.s3a.server-side-encryption-algorithm": "SSE-KMS"}
        )

        # 4. List source directory files
        files = dbutils.fs.ls("/mnt/raw_data")
        print("Found files:", [f["name"] for f in files])
        print("--- Databricks Workflow Completed Successfully ---\n")


if __name__ == "__main__":
    import unittest

    class TestDBUtils(unittest.TestCase):
        def test_dbutils_redaction_and_fs(self):
            # Run simulation
            DatabricksWorkflow.run_pipeline()

            # Direct assertions on secret retrieval
            sec_val = dbutils.secrets.get("dw-credentials-scope", "dw_password")
            
            # Must show [REDACTED] when printed/formatted
            self.assertEqual(str(sec_val), "[REDACTED]")
            self.assertEqual(repr(sec_val), "[REDACTED]")
            
            # Underlying value must match
            if hasattr(sec_val, "get_raw"):
                self.assertEqual(sec_val.get_raw(), "super_secure_dw_pass_123")
            
            # File system check
            self.assertTrue(len(dbutils.fs.ls("/any/path")) > 0)

    unittest.main(argv=[''], exit=False)
