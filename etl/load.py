import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession

load_dotenv()

spark = SparkSession.builder\
       .appName("gdp_etl_quality_gate")\
       .config("spark.jars.packages", "org.apache.hadoop:hadoop-azure:3.4.2,com.azure:azure-storage-blob:12.20.0")\
       .config("spark.hadoop.fs.azure.account.auth.type.devstoreaccount1.blob.core.windows.net", "SharedKey")\
       .config("spark.hadoop.fs.azure.account.key.devstoreaccount1.blob.core.windows.net", "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==")\
       .config("spark.hadoop.fs.azure.storage.emulator.enabled", "true")\
       .config("spark.hadoop.fs.azure.storage.emulator.account.name", "devstoreaccount1")\
       .config("spark.hadoop.fs.azure.storage.emulator.rest.endpoint", "http://127.0.0.1:10000")\
       .getOrCreate()


def create_table_bronze_gdp(rw_data: list[dict]) -> None:
    """
    Converts list of dictionaries from the extract.py file to Spark df 
    and persists as parquet in the Azurite bronze layer.
    """

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING") #access the repository and checks the .env file for connection string

    try:
        df = spark.createDataFrame(rw_data)
        df.write\
        .format("parquet")\
        .mode("overwrite")\
        .save("wasbs://bronze@devstoreaccount1/gdp_raw")
    except Exception as e:
        print(f"Errror loading bronze layer: {e}")
