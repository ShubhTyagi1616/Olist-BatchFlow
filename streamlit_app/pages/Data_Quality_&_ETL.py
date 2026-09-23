import streamlit as st
import pandas as pd  

from queries import (
    get_total_fact_records,
    get_fact_null_quality,
    get_duplicate_order_item_check,
    get_referential_integrity_checks,
    get_fact_validity_checks,
)

st.set_page_config(
    page_title="Data Quality & ETL",
    page_icon="🔍",
    layout="wide",
)

st.title("Data Quality & ETL Monitoring")
st.caption(
    "Warehouse data quality, integrity, and pipeline validation metrics."
)

st.divider()

st.subheader("Data Quality Overview")
st.caption(
    "Monitor the completeness, uniqueness, and integrity of warehouse data."
)


total_records = get_total_fact_records()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Fact Table Records",
        f"{total_records:,}"
    )


st.divider()

st.subheader("Fact Table NULL Checks")
st.caption(
    "Monitoring missing values in critical warehouse fact-table columns."
)

null_quality_df = get_fact_null_quality()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "NULL Order IDs",
        f"{int(null_quality_df.loc[0, 'null_order_id']):,}"
    )

with col2:
    st.metric(
        "NULL Customer IDs",
        f"{int(null_quality_df.loc[0, 'null_customer_id']):,}"
    )

with col3:
    st.metric(
        "NULL Seller IDs",
        f"{int(null_quality_df.loc[0, 'null_seller_id']):,}"
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "NULL Product IDs",
        f"{int(null_quality_df.loc[0, 'null_product_id']):,}"
    )

with col5:
    st.metric(
        "NULL Order Dates",
        f"{int(null_quality_df.loc[0, 'null_order_purchase_date']):,}"
    )

with col6:
    st.metric(
        "NULL Prices",
        f"{int(null_quality_df.loc[0, 'null_price']):,}"
    )


st.divider()

st.subheader("Duplicate Order-Item Check")
st.caption(
    "Checks whether the same order and order-item combination appears more than once."
)

duplicate_order_items = get_duplicate_order_item_check()

if duplicate_order_items == 0:
    st.success(
        "No duplicate order-item combinations detected."
    )
else:
    st.warning(
        f"{duplicate_order_items:,} duplicate order-item combinations detected."
    )

st.metric(
    "Duplicate Order-Item Groups",
    f"{duplicate_order_items:,}"
)


st.divider()

st.subheader("Referential Integrity Checks")
st.caption(
    "Verifies that fact-table foreign keys exist in the corresponding dimension tables."
)

referential_df = get_referential_integrity_checks()

missing_customers = int(
    referential_df.loc[0, "missing_customers"]
)

missing_sellers = int(
    referential_df.loc[0, "missing_sellers"]
)

missing_products = int(
    referential_df.loc[0, "missing_products"]
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Missing Customers",
        f"{missing_customers:,}"
    )

with col2:
    st.metric(
        "Missing Sellers",
        f"{missing_sellers:,}"
    )

with col3:
    st.metric(
        "Missing Products",
        f"{missing_products:,}"
    )


st.divider()

st.subheader("Date & Numeric Validity Checks")
st.caption(
    "Checks for unusual dates and invalid or potentially anomalous numeric values."
)

validity_df = get_fact_validity_checks()

future_order_dates = int(
    validity_df.loc[0, "future_order_dates"]
)

negative_prices = int(
    validity_df.loc[0, "negative_prices"]
)

negative_freight = int(
    validity_df.loc[0, "negative_freight"]
)

zero_price_items = int(
    validity_df.loc[0, "zero_price_items"]
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Future Order Dates",
        f"{future_order_dates:,}"
    )

with col2:
    st.metric(
        "Negative Prices",
        f"{negative_prices:,}"
    )

col3, col4 = st.columns(2)

with col3:
    st.metric(
        "Negative Freight",
        f"{negative_freight:,}"
    )

with col4:
    st.metric(
        "Zero-Price Items",
        f"{zero_price_items:,}"
    )



st.divider()

st.subheader("Data Quality Summary")
st.caption(
    "Overall status of critical warehouse data-quality checks."
)

quality_checks = {
    "NULL Order IDs": int(null_quality_df.loc[0, "null_order_id"]),
    "NULL Customer IDs": int(null_quality_df.loc[0, "null_customer_id"]),
    "NULL Seller IDs": int(null_quality_df.loc[0, "null_seller_id"]),
    "NULL Product IDs": int(null_quality_df.loc[0, "null_product_id"]),
    "NULL Order Dates": int(
        null_quality_df.loc[0, "null_order_purchase_date"]
    ),
    "NULL Prices": int(null_quality_df.loc[0, "null_price"]),
    "Duplicate Order-Item Groups": duplicate_order_items,
    "Missing Customers": missing_customers,
    "Missing Sellers": missing_sellers,
    "Missing Products": missing_products,
    "Future Order Dates": future_order_dates,
    "Negative Prices": negative_prices,
    "Negative Freight": negative_freight,
}

for check_name, issue_count in quality_checks.items():

    if issue_count == 0:
        st.success(
            f"PASS — {check_name}: No issues detected."
        )
    else:
        st.warning(
            f"WARNING — {check_name}: {issue_count:,} issue(s) detected."
        )



st.divider()

st.subheader("Overall Data Quality Score")
st.caption(
    "Percentage of configured data-quality checks that currently pass."
)

total_checks = len(quality_checks)

passed_checks = sum(
    1
    for issue_count in quality_checks.values()
    if issue_count == 0
)

data_quality_score = (
    (passed_checks / total_checks) * 100
    if total_checks > 0
    else 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Data Quality Score",
        f"{data_quality_score:.2f}%"
    )

with col2:
    st.metric(
        "Checks Passed",
        f"{passed_checks}/{total_checks}"
    )

with col3:
    st.metric(
        "Checks With Issues",
        f"{total_checks - passed_checks}"
    )



st.divider()

st.subheader("Data Quality Check Status")

status_summary = {
    "PASS": passed_checks,
    "WARNING": total_checks - passed_checks,
}

status_df = pd.DataFrame(
    {
        "Status": list(status_summary.keys()),
        "Checks": list(status_summary.values()),
    }
)

st.bar_chart(
    status_df.set_index("Status")["Checks"]
)