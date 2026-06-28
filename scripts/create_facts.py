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
def fact_events():

    events= pd.read_parquet(CLEANED_DIR / "events_cleaned.parquet")
    fact_events= events[[
    'event_id',
    'product_id',
    'session_id',
    'event_type',
    'timestamp',
    'qty',
    'cart_size',
    'payment',
    'discount_pct',
    'amount_usd',
    'event_date',
    'year',
    'month'
    ]].copy()

    fact_events.to_parquet(
        WAREHOUSE_DIR / "fact_events.parquet", index=False
        )
    
    print(f"fact_events created with {len(fact_events)} records.")

# %%
def fact_orders():
    orders = pd.read_parquet(CLEANED_DIR / "orders_cleaned.parquet")

    orders['order_date'] = pd.to_datetime(orders['order_time'].dt.date)
    orders['year'] = pd.to_datetime(orders['order_date'].dt.year)

    fact_orders= orders[[
    'order_id',
    'customer_id',
    'payment_method',
    'discount_pct',
    'subtotal_usd',
    'total_usd',
    'device',
    'country',
    'source',
    'order_date',
    'year'
    ]].copy()

    fact_orders.to_parquet(
        WAREHOUSE_DIR / "fact_orders.parquet", index=False
        )
    
    print(f"fact_orders created with {len(fact_orders)} records.")

# %%
def fact_order_items():
    order_items = pd.read_parquet(CLEANED_DIR / "order_items_cleaned.parquet")

    fact_order_items= order_items[[
    'order_id',
    'product_id',
    'quantity',
    'unit_price_usd',
    'line_total_usd'
    ]].copy()

    fact_order_items.to_parquet(
        WAREHOUSE_DIR / "fact_order_items.parquet", index=False
        )
    
    print(f"fact_order_items created with {len(fact_order_items)} records.")

# %%
def fact_sessions():

    sessions= pd.read_parquet(CLEANED_DIR / "sessions_cleaned.parquet")

    sessions['start_date'] = pd.to_datetime(sessions['start_time'].dt.year)
    sessions['start_year'] = pd.to_datetime(sessions['start_time'].dt.year)

    fact_sessions= sessions[[
    'session_id',
    'customer_id',
    'start_date',
    'start_year',
    'device',
    'country',
    'source'
    ]].copy()

    fact_sessions.to_parquet(
        WAREHOUSE_DIR / "fact_sessions.parquet", index=False
        )
    
    print(f"fact_sessions created with {len(fact_sessions)} records.")

# %%
def fact_reviews():

    reviews= pd.read_parquet(CLEANED_DIR / "reviews_cleaned.parquet")

    reviews['review_date'] = pd.to_datetime(reviews['review_time'].dt.date)
    reviews['review_year'] = pd.to_datetime(reviews['review_time'].dt.year)

    fact_reviews= reviews[[
    'review_id',
    'order_id',
    'product_id',
    'rating',
    'review_time'
    ]].copy()
    
    fact_reviews.to_parquet(
        WAREHOUSE_DIR / "fact_reviews.parquet", index=False
        )
    
    print(f"fact_reviews created with {len(fact_reviews)} records.")

# %%
def main():
    fact_events()
    fact_orders()
    fact_order_items()
    fact_sessions()
    fact_reviews()

# %%
if __name__ == "__main__":
    main()


