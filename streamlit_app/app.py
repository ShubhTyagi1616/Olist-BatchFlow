import streamlit as st
import plotly.graph_objects as go  


from queries import (
    get_total_orders,
    get_total_customers,
    get_total_sellers,
    get_total_products,
    get_total_revenue,
    get_total_freight,
    get_average_order_value,
    get_average_review_score,
    get_monthly_sales,
    get_order_status_distribution,
)


st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="📊",
    layout="wide",
)


st.title("Olist E-Commerce Analytics")
st.caption("Brazilian E-Commerce Batch Analytics Dashboard")


# =========================
# Overview KPIs
# =========================

total_orders = get_total_orders()
total_customers = get_total_customers()
total_sellers = get_total_sellers()
total_products = get_total_products()

total_revenue = get_total_revenue()
total_freight = get_total_freight()
average_order_value = get_average_order_value()
average_review_score = get_average_review_score()
monthly_sales = get_monthly_sales()


# =========================
# KPI Cards
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Orders", f"{total_orders:,}")

with col2:
    st.metric("Total Customers", f"{total_customers:,}")

with col3:
    st.metric("Total Sellers", f"{total_sellers:,}")

with col4:
    st.metric("Total Products", f"{total_products:,}")


st.divider()


col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Total Revenue", f"R$ {total_revenue:,.2f}")

with col6:
    st.metric("Total Freight", f"R$ {total_freight:,.2f}")

with col7:
    st.metric("Average Order Value", f"R$ {average_order_value:,.2f}")

with col8:
    st.metric("Average Review Score", f"{average_review_score:.2f} / 5")


st.divider()

st.subheader("Monthly Revenue & Orders")

monthly_sales = get_monthly_sales()

monthly_sales["month_label"] = (
    monthly_sales["year"].astype(str)
    + "-"
    + monthly_sales["month"].astype(str).str.zfill(2)
)

st.write("### Monthly Revenue")

st.line_chart(
    monthly_sales.set_index("month_label")["revenue"]
)

st.write("### Monthly Orders")

st.line_chart(
    monthly_sales.set_index("month_label")["total_orders"]
)

# order status distribution charts : 
st.divider()

st.subheader("Order Status Distribution")

status_df = get_order_status_distribution()

fig = go.Figure(
    data=[
        go.Pie(
            labels=status_df["order_status"],
            values=status_df["total_orders"],
            hole=0.45,
            textinfo="label+percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Orders: %{value:,}<br>"
                "Share: %{percent}<extra></extra>"
            ),
        )
    ]
)

fig.update_layout(
    title="Order Status Distribution",
    showlegend=True,
    height=450,
)

st.plotly_chart(fig, use_container_width=True)

