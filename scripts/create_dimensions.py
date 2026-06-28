# %%
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
WAREHOUSE_DIR = BASE_DIR / "data" / "warehouse"

CLEANED_DIR.mkdir(parents=True, exist_ok=True)
WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

# %%
def dim_customers():

    customers = pd.read_parquet(CLEANED_DIR / "customers_cleaned.parquet")

    dim_customers= customers[[
    'customer_id',
    'country',
    'age',
    'signup_date',
    'marketing_opt_in'
    ]].copy()
    
    dim_customers.to_parquet(
        WAREHOUSE_DIR / "dim_customers.parquet",
          index=False)

    print(
        f"dim_customers created with {len(dim_customers)} rows."
        )

# %%
def dim_products():
    products = pd.read_parquet(CLEANED_DIR / "products_cleaned.parquet")

    dim_products= products[[
    'product_id',
    'category',
    'name',
    'price_usd',
    'cost_usd',
    'margin_usd'
    ]].copy()
    
    dim_products.to_parquet(
        WAREHOUSE_DIR / "dim_products.parquet",
          index=False)

    print(
        f"dim_products created with {len(dim_products)} rows."
        )

# %%
def dim_date():

    events=pd.read_parquet(CLEANED_DIR / "events_cleaned.parquet")

    events['event_date'] = pd.to_datetime(events['event_date'])
    events['weekday'] = events['event_date'].dt.day_name()

    dim_date= events[[
    'event_date',
    'year',
    'month',
    'day',
    'weekday',
    'hour'
    ]].copy() 

    dim_date.drop_duplicates(inplace=True)
    
    dim_date.to_parquet(
        WAREHOUSE_DIR / "dim_date.parquet",
        index=False
    )

    print(
        f"dim_date created: {len(dim_date)} rows"
    )


# %%
def main():
    dim_customers()
    dim_products()
    dim_date()

# %%
if __name__ == "__main__":
    main()


