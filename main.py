from etl.spark_session import get_spark_session
from etl.extract import fetch_gdp_per_capita
from etl.load import create_table_bronze_gdp
from etl.transform import create_table_silver_gdp

if __name__ == "__main__":
    spark = get_spark_session()

    print("Accessing World Bank API...")
    rw = fetch_gdp_per_capita()

    print(f"Records extracted: {len(rw)}")

    print("Loading bronze table to storage...")
    create_table_bronze_gdp(rw, spark)#passing spar

    print("Loading silver table to storage...")
    create_table_silver_gdp(spark)

    print("Done!")