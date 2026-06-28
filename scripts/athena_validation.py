import boto3
import time

DATABASE = "funnel_db"
OUTPUT_LOCATION = "s3://funnel-analytics-result/athena-results/"

TABLES = [
    "dim_customers",
    "dim_products",
    "dim_date",
    "fact_orders",
    "fact_order_items",
    "fact_events",
    "fact_reviews",
    "fact_sessions"
]

athena = boto3.client("athena")


def validate_table(table_name):

    query = f"SELECT COUNT(*) FROM {table_name};"

    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": DATABASE},
        ResultConfiguration={"OutputLocation": OUTPUT_LOCATION},
    )

    query_execution_id = response["QueryExecutionId"]

    start_time = time.time()

    while True:

        execution = athena.get_query_execution(
            QueryExecutionId=query_execution_id
        )

        status = execution["QueryExecution"]["Status"]["State"]

        if status == "SUCCEEDED":
            break

        elif status in ["FAILED", "CANCELLED"]:

            reason = execution["QueryExecution"]["Status"].get(
                "StateChangeReason",
                "Unknown error"
            )

            raise Exception(
                f"{table_name} query failed.\nReason: {reason}"
            )

        if time.time() - start_time > 300:
            raise TimeoutError(f"{table_name} query timed out.")

        time.sleep(2)

    results = athena.get_query_results(
        QueryExecutionId=query_execution_id
    )

    rows = results["ResultSet"]["Rows"]

    if len(rows) < 2:
        raise Exception(f"{table_name} returned no result.")

    count = int(rows[1]["Data"][0]["VarCharValue"])

    if count == 0:
        raise Exception(f"{table_name} is empty.")

    print(f"✓ {table_name}: {count} rows")


def main():

    
    print("Running Athena Validation")
    

    for table in TABLES:
        validate_table(table)

    print("\nAll Athena validations passed successfully.")


if __name__ == "__main__":
    main()