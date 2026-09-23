import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
import streamlit as st  

load_dotenv()


def get_engine():
    try:
        host = st.secrets["DB_HOST"]
        port = st.secrets["DB_PORT"]
        database = st.secrets["DB_NAME"]
        user = st.secrets["DB_USER"]
        password = st.secrets["DB_PASSWORD"]
    except st.errors.StreamlitSecretNotFoundError:
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

    password = quote_plus(password)

    database_url = (
        f"postgresql+psycopg2://{user}:{password}"
        f"@{host}:{port}/{database}"
    )

    return create_engine(database_url, pool_pre_ping=True)