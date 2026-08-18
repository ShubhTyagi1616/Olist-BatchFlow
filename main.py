import os
import logging
from sqlalchemy import create_engine
from src.config import DB_URL
from src.extract import extract_all
from src.transform import transform_all
from src.load import load_to_staging, load_to_warehouse

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/etl.log"),
        logging.StreamHandler(),
    ],
    force=True,
)
logger = logging.getLogger(__name__)

def run_pipeline():
    logging.info("==== ETL PIPELINE STARTED ======")
    engine = create_engine(DB_URL)

    try:
        logger.info("Step 1: Extracting raw data...")
        raw_data = extract_all()

        logger.info("Step 2: Loading raw data into staging...")
        load_to_staging(raw_data, engine)

        logger.info("Step 3: Transforming data...")
        warehouse_data = transform_all()

        logger.info("Step 4: Loading data into warehouse...")
        load_to_warehouse(warehouse_data, engine)

        logger.info("==== ETL PIPELINE COMPLETED SUCCCESSFULLY=====")

    except Exception as err:
        logging.error(f"Pipeline failed: {err}")
        raise

if __name__=="__main__":
    run_pipeline()