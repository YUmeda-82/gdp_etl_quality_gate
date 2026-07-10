from etl.extract import fetch_gdp_per_capita
from etl.load import load_to_bronze

if __name__ == "__main__":
    print("Accessing World Bank API...")
    rw = fetch_gdp_per_capita()

    print(f"Records extracted: {len(rw)}")

    print("Loading table to storage...")
    load_to_bronze(rw)

    print("Done!")