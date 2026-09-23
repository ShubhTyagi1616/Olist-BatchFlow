import streamlit as st

from queries import (
    get_total_customers,
    get_customers_with_orders,
    get_average_orders_per_customer,
    get_customers_by_state,
    get_top_customers_by_orders,
    get_total_sellers,
    get_sellers_with_orders,
    get_average_orders_per_seller,
    get_sellers_by_state,
    get_seller_performance,
)

st.set_page_config(
    page_title="Customer & Seller Analysis",
    page_icon="👥",
    layout="wide",
)


st.title("Customer & Seller Analysis")
st.caption("Customer and seller performance analysis")


st.divider()

st.subheader("Customer & Seller Overview")


# =========================
# Customer KPIs
# =========================

total_customers = get_total_customers()
customers_with_orders = get_customers_with_orders()
average_orders_per_customer = get_average_orders_per_customer()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Customers with Orders",
        f"{customers_with_orders:,}"
    )

with col3:
    st.metric(
        "Avg Orders / Customer",
        f"{average_orders_per_customer:.2f}"
    )


st.divider()

st.subheader("Customer Distribution by State")

customer_state_df = get_customers_by_state()

st.bar_chart(
    customer_state_df.set_index("customer_state")["total_customers"],
    horizontal=True,
)

st.divider()

st.subheader("Top Customers by Orders")

top_customers_df = get_top_customers_by_orders()

st.dataframe(
    top_customers_df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

st.subheader("Seller Overview")

# Seller KPIs
total_sellers = get_total_sellers()
sellers_with_orders = get_sellers_with_orders()
average_orders_per_seller = get_average_orders_per_seller()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sellers",
        f"{total_sellers:,}"
    )

with col2:
    st.metric(
        "Sellers with Orders",
        f"{sellers_with_orders:,}"
    )

with col3:
    st.metric(
        "Avg Orders / Seller",
        f"{average_orders_per_seller:.2f}"
    )


st.divider()

st.subheader("Seller Distribution by State")

seller_state_df = get_sellers_by_state()

st.bar_chart(
    seller_state_df.set_index("seller_state")["total_sellers"],
    horizontal=True,
)


st.divider()

st.subheader("Seller Performance")

seller_performance_df = get_seller_performance()

st.dataframe(
    seller_performance_df,
    use_container_width=True,
    hide_index=True,
)