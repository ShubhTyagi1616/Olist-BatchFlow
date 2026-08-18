import logging
from sqlalchemy import create_engine
from sqlalchemy import text
from src.config import DB_URL
from src.extract import extract_all
from src.transform import transform_all

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# maps our short names --> staging table names
STAGING_TABLE_MAP = {
    "customers": "stg_customers",
    "orders": "stg_orders",
    "order_items":"stg_order_items",
    "order_payments": "stg_order_payments",
    "order_reviews": "stg_order_reviews",
    "products":"stg_products",
    "sellers": "stg_sellers",
    "geolocation":"stg_geolocation",
    "category_translation": "stg_category_translation"
}

# order matters: dims first, fact_orders last(foreign key dependency)
WAREHOUSE_LOAD_ORDER = [
    "dim_customers","dim_sellers","dim_products","dim_date","fact_orders"
]


# make method to load the data in staging table in batch_etl_db
def load_to_staging(dataframes:dict, engine):

    for name, df in dataframes.items():
        table_name = STAGING_TABLE_MAP[name]
        try:
            with engine.begin() as conn:
                df.write_database(
                    table_name=f"staging.{table_name}",
                    connection=engine,
                    if_table_exists="replace",
                )
            logger.info(f"Loaded {name} into staging.{table_name} : {df.shape[0]} row")
        except Exception as err:
            logging.error(f"Failed to load {name} into staging.{table_name}:{err}")
            raise

def load_to_warehouse(warehouse_data: dict, engine):
    # truncate in reverse order (fact tables first, since it has the FKS)
    truncate_order = ["fact_orders","dim_date","dim_products","dim_sellers","dim_customers"]

    with engine.begin() as conn:
        for table_name in truncate_order:
            conn.execute(text(f"TRUNCATE TABLE warehouse.{table_name} CASCADE"))
            logger.info(f"TRUNCATED warehouse.{table_name}")

# load in normal order(dims first, fact last) using append now that tables are empty
    for table_name in WAREHOUSE_LOAD_ORDER:
        df = warehouse_data[table_name]
        try:
            with engine.begin() as conn:
                df.write_database(
                    table_name=f"warehouse.{table_name}",
                    connection=conn,
                    if_table_exists="append",
                )
            logger.info(f"Loaded {table_name} into warehouse.{table_name}:{df.shape[0]} rows")
        except Exception as err:
            logging.error(f"Failed to load{table_name} into warehouse.{table_name}:{err}")
            raise

if __name__=="__main__":
    engine = create_engine(DB_URL)

    raw_data = extract_all()
    load_to_staging(raw_data, engine)

    warehouse_data = transform_all()
    load_to_warehouse(warehouse_data, engine)