import boto3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WAREHOUSE_DIR = BASE_DIR / "data" / "warehouse"

s3 = boto3.client("s3")
bucket_name = "funnel-analytics-data-lake"


def upload_file(local_path, s3_key):

    s3.upload_file(
        str(local_path),
        bucket_name,
        s3_key
    )

    print(
        f"Uploaded {local_path.name}"
    )

def upload_dimensions():

    upload_file(
        WAREHOUSE_DIR / "dim_customers.parquet",
        "warehouse/dim_customers/dim_customers.parquet"
    )

    upload_file(
        WAREHOUSE_DIR / "dim_products.parquet",
        "warehouse/dim_products/dim_products.parquet"
    )

    upload_file(
        WAREHOUSE_DIR / "dim_date.parquet",
        "warehouse/dim_date/dim_date.parquet"
    )

def upload_facts():

    upload_file(
        WAREHOUSE_DIR / "fact_events.parquet",
        "warehouse/fact_events/fact_events.parquet"
    )

    upload_file(
        WAREHOUSE_DIR / "fact_orders.parquet",
        "warehouse/fact_orders/fact_orders.parquet"
    )

    upload_file(
        WAREHOUSE_DIR / "fact_order_items.parquet",
        "warehouse/fact_order_items/fact_order_items.parquet"
    )

    upload_file(
        WAREHOUSE_DIR / "fact_sessions.parquet",
        "warehouse/fact_sessions/fact_sessions.parquet"
    )

    upload_file(
        WAREHOUSE_DIR / "fact_reviews.parquet",
        "warehouse/fact_reviews/fact_reviews.parquet"
    )

def main():

    upload_dimensions()

    upload_facts()

    print(
        "All warehouse files uploaded"
    )


if __name__ == "__main__":
    main()  
