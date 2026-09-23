import pandas as pd

from db import get_engine


def run_query(query: str) -> pd.DataFrame:
    """
    Execute a SQL query and return the result as a Pandas DataFrame.
    """
    engine = get_engine()
    return pd.read_sql(query, engine)


def get_total_orders(year=None, status=None):
    query = """
        SELECT
            COUNT(DISTINCT f.order_id) AS total_orders
        FROM warehouse.fact_orders f
        JOIN warehouse.dim_date d
            ON f.order_purchase_date = d.date_id
        WHERE 1=1
    """

    if year not in (None, "All"):
        query += f"""
            AND d.year = {int(year)}
        """

    if status not in (None, "All"):
        query += f"""
            AND f.order_status = '{status}'
        """

    df = run_query(query)

    return int(df.loc[0, "total_orders"])


def get_total_customers() -> int:
    query = """
        SELECT COUNT(*) AS total_customers
        FROM warehouse.dim_customers;
    """

    df = run_query(query)
    return int(df.loc[0, "total_customers"])


def get_total_sellers() -> int:
    query = """
        SELECT COUNT(*) AS total_sellers
        FROM warehouse.dim_sellers;
    """

    df = run_query(query)
    return int(df.loc[0, "total_sellers"])


def get_total_products() -> int:
    query = """
        SELECT COUNT(*) AS total_products
        FROM warehouse.dim_products;
    """

    df = run_query(query)
    return int(df.loc[0, "total_products"])


def get_total_revenue(year=None, status=None):
    query = """
        SELECT
            COALESCE(SUM(f.price), 0) AS total_revenue
        FROM warehouse.fact_orders f
        JOIN warehouse.dim_date d
            ON f.order_purchase_date = d.date_id
        WHERE 1=1
    """

    if year not in (None, "All"):
        query += f"""
            AND d.year = {int(year)}
        """

    if status not in (None, "All"):
        query += f"""
            AND f.order_status = '{status}'
        """

    df = run_query(query)

    return float(df.loc[0, "total_revenue"])


def get_total_freight() -> float:
    query = """
        SELECT COALESCE(SUM(freight_value), 0) AS total_freight
        FROM warehouse.fact_orders;
    """

    df = run_query(query)
    return float(df.loc[0, "total_freight"])


def get_average_order_value(year=None, status=None):
    query = """
        SELECT
            COALESCE(
                SUM(f.price)
                / NULLIF(COUNT(DISTINCT f.order_id), 0),
                0
            ) AS average_order_value
        FROM warehouse.fact_orders f
        JOIN warehouse.dim_date d
            ON f.order_purchase_date = d.date_id
        WHERE 1=1
    """

    if year not in (None, "All"):
        query += f"""
            AND d.year = {int(year)}
        """

    if status not in (None, "All"):
        query += f"""
            AND f.order_status = '{status}'
        """

    df = run_query(query)

    return float(df.loc[0, "average_order_value"])


def get_average_review_score() -> float:
    query = """
        SELECT COALESCE(AVG(review_score), 0) AS average_review_score
        FROM warehouse.fact_orders
        WHERE review_score IS NOT NULL;
    """

    df = run_query(query)
    return float(df.loc[0, "average_review_score"])


def get_monthly_sales(year=None, status=None):
    query = """
        SELECT
            d.year,
            d.month,
            SUM(f.price) AS revenue,
            COUNT(DISTINCT f.order_id) AS total_orders
        FROM warehouse.fact_orders f
        JOIN warehouse.dim_date d
            ON f.order_purchase_date = d.date_id
        WHERE 1=1
    """

    if year not in (None, "All"):
        query += f"""
            AND d.year = {int(year)}
        """

    if status not in (None, "All"):
        query += f"""
            AND f.order_status = '{status}'
        """

    query += """
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month;
    """

    return run_query(query)



def get_order_status_distribution():
    query = """
        SELECT
            order_status,
            COUNT(DISTINCT order_id) AS total_orders
        FROM warehouse.fact_orders
        GROUP BY order_status
        ORDER BY total_orders DESC;
    """

    return run_query(query)


def get_top_product_categories(limit=10, year=None, status=None):
    query = f"""
        SELECT
            COALESCE(
                p.product_category_english,
                'Unknown'
            ) AS category,
            SUM(f.price) AS revenue
        FROM warehouse.fact_orders f
        JOIN warehouse.dim_products p
            ON f.product_id = p.product_id
        JOIN warehouse.dim_date d
            ON f.order_purchase_date = d.date_id
        WHERE 1=1
    """

    if year not in (None, "All"):
        query += f"""
            AND d.year = {int(year)}
        """

    if status not in (None, "All"):
        query += f"""
            AND f.order_status = '{status}'
        """

    query += f"""
        GROUP BY
            COALESCE(
                p.product_category_english,
                'Unknown'
            )
        ORDER BY revenue DESC
        LIMIT {int(limit)};
    """

    return run_query(query)


def get_top_sellers(limit=10, year=None, status=None):
    query = f"""
        SELECT
            f.seller_id,
            SUM(f.price) AS revenue,
            COUNT(DISTINCT f.order_id) AS total_orders
        FROM warehouse.fact_orders f
        JOIN warehouse.dim_sellers s
            ON f.seller_id = s.seller_id
        JOIN warehouse.dim_date d
            ON f.order_purchase_date = d.date_id
        WHERE 1=1
    """

    if year not in (None, "All"):
        query += f"""
            AND d.year = {int(year)}
        """

    if status not in (None, "All"):
        query += f"""
            AND f.order_status = '{status}'
        """

    query += f"""
        GROUP BY f.seller_id
        ORDER BY revenue DESC
        LIMIT {int(limit)};
    """

    return run_query(query)



def get_customers_with_orders():
    query = """
        SELECT COUNT(DISTINCT customer_id) AS customers_with_orders
        FROM warehouse.fact_orders;
    """

    df = run_query(query)
    return int(df.loc[0, "customers_with_orders"])


def get_average_orders_per_customer():
    query = """
        SELECT
            COALESCE(
                COUNT(DISTINCT order_id)::NUMERIC
                / NULLIF(COUNT(DISTINCT customer_id), 0),
                0
            ) AS average_orders_per_customer
        FROM warehouse.fact_orders;
    """

    df = run_query(query)
    return float(df.loc[0, "average_orders_per_customer"])


def get_customers_by_state(limit=10):
    query = f"""
        SELECT
            customer_state,
            COUNT(*) AS total_customers
        FROM warehouse.dim_customers
        WHERE customer_state IS NOT NULL
        GROUP BY customer_state
        ORDER BY total_customers DESC
        LIMIT {limit};
    """

    return run_query(query)


def get_top_customers_by_orders(limit=10):
    query = f"""
        SELECT
            f.customer_id,
            c.customer_unique_id,
            c.customer_city,
            c.customer_state,
            COUNT(DISTINCT f.order_id) AS total_orders
        FROM warehouse.fact_orders f
        JOIN warehouse.dim_customers c
            ON f.customer_id = c.customer_id
        GROUP BY
            f.customer_id,
            c.customer_unique_id,
            c.customer_city,
            c.customer_state
        ORDER BY total_orders DESC
        LIMIT {limit};
    """

    return run_query(query)


def get_sellers_with_orders():
    query = """
        SELECT COUNT(DISTINCT seller_id) AS sellers_with_orders
        FROM warehouse.fact_orders;
    """
    df = run_query(query)
    return int(df.loc[0, "sellers_with_orders"])


def get_average_orders_per_seller():
    query = """
        SELECT
            COALESCE(
                COUNT(DISTINCT order_id)::NUMERIC
                / NULLIF(COUNT(DISTINCT seller_id), 0),
                0
            ) AS average_orders_per_seller
        FROM warehouse.fact_orders;
    """
    df = run_query(query)
    return float(df.loc[0, "average_orders_per_seller"])


def get_sellers_by_state(limit=10):
    query = f"""
        SELECT
            seller_state,
            COUNT(*) AS total_sellers
        FROM warehouse.dim_sellers
        WHERE seller_state IS NOT NULL
        GROUP BY seller_state
        ORDER BY total_sellers DESC
        LIMIT {limit};
    """
    return run_query(query)


def get_seller_performance(limit=20):
    query = f"""
        SELECT
            f.seller_id,
            s.seller_city,
            s.seller_state,
            SUM(f.price) AS revenue,
            COUNT(DISTINCT f.order_id) AS total_orders,
            COALESCE(
                SUM(f.price)
                / NULLIF(COUNT(DISTINCT f.order_id), 0),
                0
            ) AS average_order_value
        FROM warehouse.fact_orders f
        JOIN warehouse.dim_sellers s
            ON f.seller_id = s.seller_id
        GROUP BY
            f.seller_id,
            s.seller_city,
            s.seller_state
        ORDER BY revenue DESC
        LIMIT {limit};
    """
    return run_query(query)


def get_total_reviewed_orders():
    query = """
        SELECT COUNT(DISTINCT order_id) AS reviewed_orders
        FROM warehouse.fact_orders
        WHERE review_score IS NOT NULL;
    """
    df = run_query(query)
    return int(df.loc[0, "reviewed_orders"])


def get_positive_review_percentage():
    query = """
        SELECT
            COALESCE(
                100.0 * COUNT(DISTINCT CASE
                    WHEN review_score IN (4, 5) THEN order_id
                END)
                / NULLIF(COUNT(DISTINCT CASE
                    WHEN review_score IS NOT NULL THEN order_id
                END), 0),
                0
            ) AS positive_review_percentage
        FROM warehouse.fact_orders;
    """
    df = run_query(query)
    return float(df.loc[0, "positive_review_percentage"])


def get_review_score_distribution():
    query = """
        SELECT
            review_score,
            COUNT(DISTINCT order_id) AS total_orders
        FROM warehouse.fact_orders
        WHERE review_score IS NOT NULL
        GROUP BY review_score
        ORDER BY review_score;
    """
    return run_query(query)


def get_review_score_by_order_status():
    query = """
        SELECT
            order_status,
            COUNT(DISTINCT order_id) AS total_orders,
            ROUND(AVG(review_score), 2) AS average_review_score
        FROM warehouse.fact_orders
        WHERE review_score IS NOT NULL
        GROUP BY order_status
        ORDER BY average_review_score DESC;
    """
    return run_query(query)



def get_delivery_performance():
    query = """
        SELECT
            f.order_status,
            COUNT(DISTINCT f.order_id) AS total_orders,
            ROUND(
                AVG(
                    EXTRACT(
                        EPOCH FROM (
                            o.order_delivered_customer_date
                            - f.order_purchase_date
                        )
                    ) / 86400.0
                )::NUMERIC,
                2
            ) AS avg_delivery_days
        FROM warehouse.fact_orders f
        JOIN staging.stg_orders o
            ON f.order_id = o.order_id
        WHERE
            o.order_delivered_customer_date IS NOT NULL
            AND f.order_purchase_date IS NOT NULL
        GROUP BY f.order_status
        ORDER BY avg_delivery_days;
    """
    return run_query(query)


def get_on_time_delivery_metrics():
    query = """
        SELECT
            COUNT(DISTINCT o.order_id) AS delivered_orders,

            COUNT(DISTINCT CASE
                WHEN o.order_delivered_customer_date
                     <= o.order_estimated_delivery_date
                THEN o.order_id
            END) AS on_time_orders,

            COUNT(DISTINCT CASE
                WHEN o.order_delivered_customer_date
                     > o.order_estimated_delivery_date
                THEN o.order_id
            END) AS late_orders,

            COALESCE(
                100.0 *
                COUNT(DISTINCT CASE
                    WHEN o.order_delivered_customer_date
                         <= o.order_estimated_delivery_date
                    THEN o.order_id
                END)
                / NULLIF(COUNT(DISTINCT o.order_id), 0),
                0
            ) AS on_time_delivery_percentage

        FROM staging.stg_orders o
        WHERE
            o.order_delivered_customer_date IS NOT NULL
            AND o.order_estimated_delivery_date IS NOT NULL;
    """

    df = run_query(query)

    return {
        "delivered_orders": int(df.loc[0, "delivered_orders"]),
        "on_time_orders": int(df.loc[0, "on_time_orders"]),
        "late_orders": int(df.loc[0, "late_orders"]),
        "on_time_delivery_percentage": float(
            df.loc[0, "on_time_delivery_percentage"]
        ),
    }


def get_delivery_delay_analysis():
    query = """
        SELECT
            CASE
                WHEN o.order_delivered_customer_date
                     <= o.order_estimated_delivery_date
                THEN 'On-Time / Early'
                ELSE 'Late'
            END AS delivery_status,

            COUNT(DISTINCT o.order_id) AS total_orders,

            ROUND(
                AVG(
                    EXTRACT(
                        EPOCH FROM (
                            o.order_delivered_customer_date
                            - o.order_estimated_delivery_date
                        )
                    ) / 86400.0
                )::NUMERIC,
                2
            ) AS avg_delay_days

        FROM staging.stg_orders o

        WHERE
            o.order_delivered_customer_date IS NOT NULL
            AND o.order_estimated_delivery_date IS NOT NULL

        GROUP BY
            CASE
                WHEN o.order_delivered_customer_date
                     <= o.order_estimated_delivery_date
                THEN 'On-Time / Early'
                ELSE 'Late'
            END

        ORDER BY avg_delay_days;
    """

    return run_query(query)


def get_review_vs_delivery_performance():
    query = """
        SELECT
            CASE
                WHEN o.order_delivered_customer_date
                     <= o.order_estimated_delivery_date
                THEN 'On-Time / Early'
                ELSE 'Late'
            END AS delivery_status,

            COUNT(DISTINCT o.order_id) AS total_orders,

            ROUND(
                AVG(f.review_score)::NUMERIC,
                2
            ) AS average_review_score

        FROM warehouse.fact_orders f

        JOIN staging.stg_orders o
            ON f.order_id = o.order_id

        WHERE
            o.order_delivered_customer_date IS NOT NULL
            AND o.order_estimated_delivery_date IS NOT NULL
            AND f.review_score IS NOT NULL

        GROUP BY
            CASE
                WHEN o.order_delivered_customer_date
                     <= o.order_estimated_delivery_date
                THEN 'On-Time / Early'
                ELSE 'Late'
            END

        ORDER BY average_review_score DESC;
    """

    return run_query(query)


def get_total_fact_records():
    query = """
        SELECT COUNT(*) AS total_records
        FROM warehouse.fact_orders;
    """

    df = run_query(query)

    return int(df.loc[0, "total_records"])


def get_fact_null_quality():
    query = """
        SELECT
            COUNT(*) AS total_records,

            COUNT(*) FILTER (
                WHERE order_id IS NULL
            ) AS null_order_id,

            COUNT(*) FILTER (
                WHERE customer_id IS NULL
            ) AS null_customer_id,

            COUNT(*) FILTER (
                WHERE seller_id IS NULL
            ) AS null_seller_id,

            COUNT(*) FILTER (
                WHERE product_id IS NULL
            ) AS null_product_id,

            COUNT(*) FILTER (
                WHERE order_purchase_date IS NULL
            ) AS null_order_purchase_date,

            COUNT(*) FILTER (
                WHERE price IS NULL
            ) AS null_price

        FROM warehouse.fact_orders;
    """

    return run_query(query)


def get_duplicate_order_item_check():
    query = """
        SELECT
            COUNT(*) AS duplicate_groups
        FROM (
            SELECT
                order_id,
                order_item_id
            FROM warehouse.fact_orders
            GROUP BY
                order_id,
                order_item_id
            HAVING COUNT(*) > 1
        ) duplicates;
    """

    df = run_query(query)

    return int(df.loc[0, "duplicate_groups"])


def get_referential_integrity_checks():
    query = """
        SELECT
            COUNT(*) FILTER (
                WHERE c.customer_id IS NULL
            ) AS missing_customers,

            COUNT(*) FILTER (
                WHERE s.seller_id IS NULL
            ) AS missing_sellers,

            COUNT(*) FILTER (
                WHERE p.product_id IS NULL
            ) AS missing_products

        FROM warehouse.fact_orders f

        LEFT JOIN warehouse.dim_customers c
            ON f.customer_id = c.customer_id

        LEFT JOIN warehouse.dim_sellers s
            ON f.seller_id = s.seller_id

        LEFT JOIN warehouse.dim_products p
            ON f.product_id = p.product_id;
    """

    return run_query(query)


def get_fact_validity_checks():
    query = """
        SELECT
            COUNT(*) FILTER (
                WHERE order_purchase_date > CURRENT_DATE
            ) AS future_order_dates,

            COUNT(*) FILTER (
                WHERE price < 0
            ) AS negative_prices,

            COUNT(*) FILTER (
                WHERE freight_value < 0
            ) AS negative_freight,

            COUNT(*) FILTER (
                WHERE price = 0
            ) AS zero_price_items

        FROM warehouse.fact_orders;
    """

    return run_query(query)




# Interactive Filters : 
def get_available_years():
    query = """
        SELECT DISTINCT
            year
        FROM warehouse.dim_date
        WHERE year IS NOT NULL
        ORDER BY year;
    """

    df = run_query(query)

    return df["year"].tolist()



def get_available_order_statuses():
    query = """
        SELECT DISTINCT
            order_status
        FROM warehouse.fact_orders
        WHERE order_status IS NOT NULL
        ORDER BY order_status;
    """

    df = run_query(query)

    return df["order_status"].tolist()