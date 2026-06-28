# %%
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

CLEANED_DIR.mkdir(parents=True, exist_ok=True)

# %%
def clean_customers():

    customers = pd.read_csv(
        RAW_DIR / "customers.csv",
        encoding="latin-1"
    )

    null_count= customers.isnull().sum().sum()
    print(f"Null values in customers: {null_count}")

    duplicate_count = customers.duplicated().sum()
    if duplicate_count > 0:
        print(f"Removing {duplicate_count} duplicate rows")
        customers = customers.drop_duplicates()
    else:
        print("No duplicate rows found")
        
    customers = customers.drop(
        columns=["name","email"]
    )

    customers["signup_date"] = pd.to_datetime(
        customers["signup_date"]
    )

    customers["country"] = (
        customers["country"]
        .str.strip()
        .str.upper()
    )

    customers.to_parquet(
        CLEANED_DIR /
        "customers_cleaned.parquet",
        index=False
    )

    print(
        f"Customers cleaned: {len(customers)}"
    )

# %%
def clean_events():

    events = pd.read_csv(
        RAW_DIR / "events.csv",
        encoding="latin-1"
    )

    null_count= events.isnull().sum().sum()
    print(f"Null values in events: {null_count}")

    duplicate_count = events.duplicated().sum()
    if duplicate_count > 0:
        print(f"Removing {duplicate_count} duplicate rows")
        events = events.drop_duplicates()
    else:
        print("No duplicate rows found")

    events['timestamp'] = pd.to_datetime(events['timestamp'])

    events['event_type'] = events['event_type'].str.lower().str.strip()
    events['payment']= events['payment'].str.title().str.strip()

    events['event_date'] = events['timestamp'].dt.date
    events['year'] = events['timestamp'].dt.year
    events['month'] = events['timestamp'].dt.month
    events['day'] = events['timestamp'].dt.day
    events['hour'] = events['timestamp'].dt.hour



    events.to_parquet(
        CLEANED_DIR /
        "events_cleaned.parquet",
        index=False
    )

    print(
        f"Events cleaned: {len(events)}"
    )

# %%
def clean_sessions():

    sessions = pd.read_csv(
        RAW_DIR / "sessions.csv",
        encoding="latin-1"
    )

    null_count= sessions.isnull().sum().sum()
    print(f"Null values in sessions: {null_count}")

    duplicate_count = sessions.duplicated().sum()
    if duplicate_count > 0:
        print(f"Removing {duplicate_count} duplicate rows")
        sessions = sessions.drop_duplicates()
    else:
        print("No duplicate rows found")

    sessions['device'] = sessions['device'].str.strip().str.lower()   

    sessions["start_time"] = pd.to_datetime(
        sessions["start_time"]
    )
    sessions.to_parquet(
        CLEANED_DIR /
        "sessions_cleaned.parquet",
        index=False
    )

    print(
        f"Sessions cleaned: {len(sessions)}"
    )

# %%
def clean_products():

    products = pd.read_csv(
        RAW_DIR / "products.csv",
        encoding="latin-1"
    )

    null_count= products.isnull().sum().sum()
    print(f"Null values in products: {null_count}")
    duplicate_count = products.duplicated().sum()
    if duplicate_count > 0:
        print(f"Removing {duplicate_count} duplicate rows")
        products = products.drop_duplicates()
    else:
        print("No duplicate rows found")


    products['category'] = products['category'].str.title().str.strip()

    products.to_parquet(
        CLEANED_DIR /
        "products_cleaned.parquet",
        index=False
    )

    print(
        f"Products cleaned: {len(products)}"
    )

# %%
def clean_orders():
    orders = pd.read_csv(
        RAW_DIR / "orders.csv",
        encoding="latin-1"
    )

    null_count= orders.isnull().sum().sum()
    print(f"Null values in orders: {null_count}")

    duplicate_count = orders.duplicated().sum()
    if duplicate_count > 0:
        print(f"Removing {duplicate_count} duplicate rows")
        orders = orders.drop_duplicates()
    else:
        print("No duplicate rows found")

    orders['payment_method'] = orders['payment_method'].str.strip().str.lower()
    orders['country'] = orders['country'].str.strip()
    orders['device'] = orders['device'].str.strip().str.lower()
    orders['source'] = orders['source'].str.strip().str.lower()

    orders= orders[orders['total_usd'] > 0]
    orders= orders[(orders['discount_pct']>=0) & (orders['discount_pct']<=100)]


    orders["order_time"] = pd.to_datetime(
        orders["order_time"]
    )

    orders.to_parquet(
        CLEANED_DIR /
        "orders_cleaned.parquet",
        index=False
    )

    print(
        f"Orders cleaned: {len(orders)}"
    )

# %%
def clean_order_items():
    order_items = pd.read_csv(
        RAW_DIR / "order_items.csv",
        encoding="latin-1"
    )

    null_count= order_items.isnull().sum().sum()
    print(f"Null values in order_items: {null_count}")

    duplicate_count = order_items.duplicated().sum()
    if duplicate_count > 0:
        print(f"Removing {duplicate_count} duplicate rows from order_items")
        order_items = order_items.drop_duplicates()
    else:
        print("No duplicate rows found in order_items")

    order_items= order_items[order_items['quantity'] > 0]
    order_items= order_items[order_items['unit_price_usd'] > 0]

    order_items.to_parquet(
        CLEANED_DIR /
        "order_items_cleaned.parquet",
        index=False
    )

    print(
        f"Order items cleaned: {len(order_items)}"
    )

# %%
def clean_reviews():
    reviews = pd.read_csv(
        RAW_DIR / "reviews.csv",
        encoding="latin-1"
    )

    null_count= reviews.isnull().sum().sum()
    print(f"Null values in reviews: {null_count}")
    
    duplicate_count = reviews.duplicated().sum()
    if duplicate_count > 0:
        print(f"Removing {duplicate_count} duplicate rows")
        reviews = reviews.drop_duplicates()
    else:
        print("No duplicate rows found")

    reviews['review_text'] = reviews['review_text'].str.strip()

    reviews["review_time"] = pd.to_datetime(
        reviews["review_time"]
    )

    reviews['review_time'] = pd.to_datetime(reviews['review_time'])
    reviews= reviews[(reviews['rating'] > 0) & (reviews['rating'] <= 5)]

    reviews.to_parquet(
        CLEANED_DIR /
        "reviews_cleaned.parquet",
        index=False
    )

    print(
        f"Reviews cleaned: {len(reviews)}"
    )

# %%
def main():
    clean_customers()   
    clean_events()
    clean_sessions()
    clean_products()
    clean_orders()
    clean_order_items()
    clean_reviews()

# %%
if __name__ == "__main__":
    main()

