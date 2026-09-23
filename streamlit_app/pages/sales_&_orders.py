import streamlit as st

from queries import (
    get_total_revenue,
    get_total_orders,
    get_average_order_value,
    get_monthly_sales,
    get_top_product_categories,
    get_top_sellers,
    get_available_years,
    get_available_order_statuses,

)


st.set_page_config(
    page_title="Sales & Orders",
    page_icon="💰",
    layout="wide",
)


st.title("Sales & Orders")
st.caption(
    "Interactive sales analysis with year and order-status filters."
)



st.subheader("Filters")
st.caption("Use the filters below to analyze sales performance by year and order status.")

col1, col2 = st.columns(2)

with col1:
    available_years = get_available_years()

    selected_year = st.selectbox(
        "Select Year",
        options=["All"] + available_years
    )

with col2:
    available_statuses = get_available_order_statuses()

    selected_status = st.selectbox(
        "Select Order Status",
        options=["All"] + available_statuses
    )



st.divider()


# =========================
# Sales KPIs
# =========================

total_revenue = get_total_revenue(
    year=selected_year,
    status=selected_status
)

total_orders = get_total_orders(
    year=selected_year,
    status=selected_status
)

average_order_value = get_average_order_value(
    year=selected_year,
    status=selected_status
)

st.subheader("Sales Performance")
st.caption(
    "Key sales metrics based on the selected year and order status."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Revenue",
        f"R$ {total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "Average Order Value",
        f"R$ {average_order_value:,.2f}"
    )


st.divider()

st.subheader("Sales Trends")
st.caption(
    "Monthly revenue and order volume based on the selected filters."
)

monthly_sales = get_monthly_sales(year=selected_year,status=selected_status)

monthly_sales["month_label"] = (
    monthly_sales["year"].astype(str)
    + "-"
    + monthly_sales["month"].astype(str).str.zfill(2)
)

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.markdown("### Monthly Revenue")

    st.line_chart(
    monthly_sales.set_index("month_label")["revenue"]
)


with chart_col2:
    st.markdown("### Monthly Orders")

    st.line_chart(
    monthly_sales.set_index("month_label")["total_orders"]
)



st.divider()

st.subheader("Top Categories & Sellers")
st.caption(
    "Top-performing product categories and sellers based on the selected filters."
)

category_col, seller_col = st.columns(2)

category_df = get_top_product_categories(year=selected_year,status=selected_status)

with category_col:
    st.markdown("**Top Product Categories**")
    st.bar_chart(
    category_df.set_index("category")["revenue"]
)

st.divider()

seller_df = get_top_sellers(year=selected_year,status=selected_status)

with seller_col:
    st.markdown("**Top Sellers by Revenue**")
    st.bar_chart(
    seller_df.set_index("seller_id")["revenue"]
)
