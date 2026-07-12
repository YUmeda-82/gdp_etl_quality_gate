import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession

load_dotenv()

def create_table_bronze_gdp(rw_data: list[dict], spark: SparkSession) -> None:
    """
    Converts list of dictionaries from the extract.py file to Spark df 
    and persists as parquet in the Azurite bronze layer.
    """
    try:
        df = spark.createDataFrame(rw_data)
        df.write\
            .format("parquet")\
            .mode("overwrite")\
            .save("wasbs://bronze@devstoreaccount1/gdp_raw")
    except Exception as e:
        print(f"Error loading bronze layer: {e}")