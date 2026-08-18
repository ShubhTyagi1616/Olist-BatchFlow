import polars as pl  
import logging
from src.config import RAW_DATA_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FILE_MAP = {
    "customers":"olist_customers_dataset.csv",
    "geolocation":"olist_geolocation_dataset.csv",
    "order_items":"olist_order_items_dataset.csv",
    "order_payments":"olist_order_payments_dataset.csv",
    "order_reviews":"olist_order_reviews_dataset.csv",
    "orders":"olist_orders_dataset.csv",
    "products":"olist_products_dataset.csv",
    "sellers":"olist_sellers_dataset.csv",
    "category_translation":"product_category_name_translation.csv"
}


def extract_all() -> dict[str, pl.DataFrame]:
    """ Read all raw olist csv's into a dict of polars dataframes """
    dataframes = {}

    for name,filename in FILE_MAP.items():
        file_path = RAW_DATA_DIR / filename
        try:
            df = pl.read_csv(file_path, try_parse_dates=True)
            dataframes[name]= df
            logger.info(f"Extracted {name}: {df.shape[0]} rows, {df.shape[1]} cols")
        except Exception as err:
            logger.error(f"Failed to extract {name} from {file_path}: {err}")
            raise

    return dataframes

if __name__ == "__main__":
    data = extract_all()
    print(data["orders"].head())