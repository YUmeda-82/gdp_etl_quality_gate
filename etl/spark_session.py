from pyspark.sql import SparkSession

def get_spark_session() -> SparkSession:
    """
    Creates or reuses a SparkSession configured for Azurite local storage.
    """
    return SparkSession.builder\
           .appName("gdp_etl_quality_gate")\
           .config("spark.jars.packages", "org.apache.hadoop:hadoop-azure:3.4.2,com.azure:azure-storage-blob:12.20.0")\
           .config("spark.hadoop.fs.azure.account.auth.type.devstoreaccount1.blob.core.windows.net", "SharedKey")\
           .config("spark.hadoop.fs.azure.account.key.devstoreaccount1.blob.core.windows.net", "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==")\
           .config("spark.hadoop.fs.azure.storage.emulator.enabled", "true")\
           .config("spark.hadoop.fs.azure.storage.emulator.account.name", "devstoreaccount1")\
           .config("spark.hadoop.fs.azure.storage.emulator.rest.endpoint", "http://127.0.0.1:10000")\
           .getOrCreate()