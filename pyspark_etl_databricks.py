# ============================================================================
# PROJECT: E-Commerce Big Data Pipeline using PySpark & Databricks
# FILE: pyspark_etl_databricks.py
# DESCRIPTION: Production-grade PySpark script to extract raw CSV files,
#              apply transformations, and load into Databricks Delta Tables.
# ============================================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, current_timestamp

# 1. Initialize Spark Session (Automatically handled in Databricks, but good practice for GitHub)
spark = SparkSession.builder \
    .appName("Olist-ECommerce-BigData-ETL") \
    .getOrCreate()

print("--- PySpark Big Data Pipeline Started on Databricks ---")

# 2. Define Data Paths 
# In production, these paths usually point to Cloud Storage like AWS S3 or Azure ADLS (e.g., "dbfs:/mnt/data/")
input_base_path = "dbfs:/FileStore/tables/archive/"  # Databricks File System path
output_delta_path = "dbfs:/user/hive/warehouse/ecommerce_dw.db/"

# 3. Dictionary of files to process (Input File -> Target Delta Table)
datasets = {
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_customers_dataset.csv": "customers",
    "olist_products_dataset.csv": "products"
}

# 4. Run the Scalable ETL Loop
for file_name, table_name in datasets.items():
    source_path = f"{input_base_path}{file_name}"
    
    try:
        print(f"Processing: {file_name} -> Delta Table: {table_name}...")
        
        # [A] EXTRACTION: Read CSV with PySpark (Optimized with Schema Inference)
        df = spark.read.format("csv") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .load(source_path)
            
        # [B] TRANSFORMATION: Handle Data Types & Quality Upstream
        # If processing the orders table, explicitly cast the text date into Timestamp type
        if table_name == "orders":
            df = df.withColumn("order_purchase_timestamp", to_timestamp(col("order_purchase_timestamp")))
            
        # Add metadata column for auditing (Production Standard)
        df = df.withColumn("ingested_at", current_timestamp())

        # [C] LOADING: Save as Delta Table (Provides ACID transactions and fast performance)
        df.write.format("delta") \
            .mode("overwrite") \
            .saveAsTable(f"ecommerce_dw.{table_name}")
            
        print(f" Successfully loaded {table_name} into Delta Lake!")
        
    except Exception as e:
        print(f"❌ Error processing {file_name}: {str(e)}")

print("--- PySpark Big Data Pipeline Successfully Completed! ---")
