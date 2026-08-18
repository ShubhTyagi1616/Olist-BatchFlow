import logging
import polars as pl  
from sqlalchemy import create_engine
from src.config import DB_URL


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_staging(engine) -> dict[str,pl.DataFrame]:
    """ read all staging tables back into polars dataframe """

    tables = [
        "stg_customers","stg_orders","stg_order_items","stg_order_payments",
        "stg_order_reviews","stg_products","stg_sellers","stg_category_translation"
    ]

    data = {}
    for t in tables:
        query = f"select * from staging.{t}"
        data[t] = pl.read_database(query=query, connection=engine)
        logger.info(f"Read {t}: {data[t].shape[0]} rows")
    return data

def build_dim_customers(stg:dict) -> pl.DataFrame:
    return stg["stg_customers"].select(
        ["customer_id","customer_unique_id","customer_city","customer_state"]
    ).unique(subset=["customer_id"])

def build_dim_sellers(stg:dict) -> pl.DataFrame:
    return stg["stg_sellers"].select(
        ["seller_id","seller_city","seller_state"]
    ).unique(subset=["seller_id"])


def build_dim_products(stg:dict) -> pl.DataFrame:
    products = stg["stg_products"]
    translation = stg["stg_category_translation"]

    merged = products.join(translation, on="product_category_name", how="left")

    return merged.select([
            "product_id",
            pl.col("product_category_name_english").alias("product_category_english"),
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ]).unique(subset=["product_id"])

def build_dim_date(stg:dict) -> pl.DataFrame:
    orders = stg["stg_orders"]
    dates = orders.select(
        pl.col("order_purchase_timestamp").dt.date().alias("date_id")
    ).unique().drop_nulls()

    return dates.with_columns([
        pl.col("date_id").dt.year().alias("year"),
        pl.col("date_id").dt.month().alias("month"),
        pl.col("date_id").dt.day().alias("day"),
        pl.col("date_id").dt.strftime("%A").alias("weekday"),
    ])

def build_fact_orders(stg:dict) -> pl.DataFrame:
    orders = stg["stg_orders"]
    order_items = stg["stg_order_items"]
    payments = stg["stg_order_payments"]
    reviews = stg["stg_order_reviews"]

    # aggregate payments per order (an order can have multiple payments rows)
    payments_agg = payments.group_by("order_id").agg(
        pl.col("payment_value").sum().alias("payment_value")
    )

    # keep only one review score per order(take first if duplicates exist)
    reviews_dedup = reviews.select(["order_id","review_score"]).unique(
        subset=["order_id"], keep="first"
    )

    fact = (
        order_items
        .join(orders.select([
            "order_id","customer_id","order_status","order_purchase_timestamp"
        ]), on="order_id", how="left")
        .join(payments_agg, on="order_id", how="left")
        .join(reviews_dedup, on="order_id", how="left")
        .with_columns(
            pl.col("order_purchase_timestamp").dt.date().alias("order_purchase_date")
        )
        .select([
            "order_id","order_item_id","customer_id","seller_id","product_id",
            "order_purchase_date","order_status","price","freight_value","payment_value","review_score",
        ])
    )
    return fact

def transform_all() -> dict[str , pl.DataFrame]:
    engine = create_engine(DB_URL)
    stg = read_staging(engine)

    warehouse_data = {
        "dim_customers":build_dim_customers(stg),
        "dim_sellers":build_dim_sellers(stg),
        "dim_products":build_dim_products(stg),
        "dim_date":build_dim_date(stg),
        "fact_orders":build_fact_orders(stg),

    }

    for name , df in warehouse_data.items():
        logger.info(f"Built {name}: {df.shape[0]} row, {df.shape[1]} cols")

    return warehouse_data

if __name__=="__main__":
    data = transform_all()
    print(data["fact_orders"].head())
    
