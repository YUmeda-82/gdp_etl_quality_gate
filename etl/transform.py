from pyspark.sql import SparkSession, DataFrame

def create_table_silver_gdp(spark: SparkSession) -> DataFrame:
    """
    Reads raw GDP data from bronze layer, applies column selection
    and renaming, and persists cleaned data to silver layer.
    """
    df = spark.read.parquet("wasbs://bronze@devstoreaccount1/gdp_raw")
    df.createOrReplaceTempView("bronze_gdp")

    df_silver = spark.sql("""SELECT country.value AS COUNTRY
                                   ,country.id AS COUNTRY_ID
                                   ,indicator.id AS INDICATOR_CODE
                                   ,date AS YEAR
                                   ,ROUND(value, 2) AS VALUE_USD
                             FROM bronze_gdp
                             ORDER BY country ASC
                                     ,year DESC""")

    try:
        df_silver.write\
            .format("parquet")\
            .mode("overwrite")\
            .save("wasbs://silver@devstoreaccount1/gdp_treated")
    except Exception as e:
        print(f"Error loading silver layer: {e}")

    return df_silver