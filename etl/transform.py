from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder\
        .appName("gdp_etl_quality_gate")\
        .getOrCreate()

def transform_rw_data(raw_data: list[dict]):
    df_rw = spark.createDataFrame(raw_data)