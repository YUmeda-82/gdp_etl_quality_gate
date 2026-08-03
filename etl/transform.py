from azure.core.exceptions import AzureError
from pyspark.sql import DataFrame, SparkSession


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
        df_silver.write.format("parquet").mode("overwrite").save(
            "wasbs://silver@devstoreaccount1/gdp_treated"
        )
    except AzureError as e:
        print(f"Azure storage error: {e}")
    except Exception as e:  # noqa: BLE001
        print(f"Unexpected error loading silver layer: {e}")

    return df_silver
