import streamlit as st
import pandas as pd  

from queries import (
    get_average_review_score,
    get_total_reviewed_orders,
    get_positive_review_percentage,
    get_review_score_distribution,
    get_review_score_by_order_status,
    get_order_status_distribution,
    get_delivery_performance,
    get_on_time_delivery_metrics,
    get_delivery_delay_analysis,
    get_review_vs_delivery_performance,
)

st.set_page_config(
    page_title="Reviews & Order Status",
    page_icon="⭐",
    layout="wide",
)

st.title("Reviews & Order Status Analysis")
st.caption("Customer review and order status analysis")

st.divider()

st.subheader("Review & Order Status Overview")
st.caption(
    "Overview of customer reviews, order statuses, and overall delivery performance."
)


# Review KPIs
average_review_score = get_average_review_score()
total_reviewed_orders = get_total_reviewed_orders()
positive_review_percentage = get_positive_review_percentage()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Review Score",
        f"{average_review_score:.2f} / 5"
    )

with col2:
    st.metric(
        "Reviewed Orders",
        f"{total_reviewed_orders:,}"
    )

with col3:
    st.metric(
        "Positive Review %",
        f"{positive_review_percentage:.2f}%"
    )


st.divider()

st.subheader("Review Score Distribution")
st.caption(
    "Distribution of customer review scores across completed orders."
)

review_score_df = get_review_score_distribution()

st.bar_chart(
    review_score_df.set_index("review_score")["total_orders"]
)


st.divider()

st.subheader("Review Score by Order Status")

review_status_df = get_review_score_by_order_status()

st.dataframe(
    review_status_df,
    use_container_width=True,
    hide_index=True,
)


st.divider()

st.subheader("Order Status Distribution")

status_df = get_order_status_distribution()

st.bar_chart(
    status_df.set_index("order_status")["total_orders"],
    horizontal=True,
)


st.divider()

st.subheader("Delivery Performance")
st.caption(
    "Average delivery time across different order statuses."
)

delivery_df = get_delivery_performance()

st.dataframe(
    delivery_df,
    use_container_width=True,
    hide_index=True,
)


st.divider()

st.subheader("On-Time Delivery Performance")

delivery_metrics = get_on_time_delivery_metrics()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Delivered Orders",
        f"{delivery_metrics['delivered_orders']:,}"
    )

with col2:
    st.metric(
        "On-Time Orders",
        f"{delivery_metrics['on_time_orders']:,}"
    )

with col3:
    st.metric(
        "Late Orders",
        f"{delivery_metrics['late_orders']:,}"
    )

with col4:
    st.metric(
        "On-Time Delivery %",
        f"{delivery_metrics['on_time_delivery_percentage']:.2f}%"
    )


st.divider()

st.subheader("On-Time vs Late Deliveries")
st.caption(
    "Comparison of orders delivered on or before the estimated delivery date versus late deliveries."
)

delivery_chart_df = pd.DataFrame({
    "delivery_status": [
        "On-Time",
        "Late",
    ],
    "total_orders": [
        delivery_metrics["on_time_orders"],
        delivery_metrics["late_orders"],
    ],
})

st.bar_chart(
    delivery_chart_df.set_index("delivery_status")["total_orders"]
)


st.divider()

st.subheader("Delivery Delay Analysis")
st.caption(
    "Analysis of delivery timing against the estimated delivery date."
)

delivery_delay_df = get_delivery_delay_analysis()

st.dataframe(
    delivery_delay_df,
    use_container_width=True,
    hide_index=True,
)


st.divider()

st.subheader("Customer Review vs Delivery Performance")
st.caption(
    "Comparison of customer satisfaction between on-time and late deliveries."
)

review_delivery_df = get_review_vs_delivery_performance()

st.dataframe(
    review_delivery_df,
    use_container_width=True,
    hide_index=True,
)


st.subheader("Average Review Score by Delivery Performance")

review_chart_df = review_delivery_df[
    ["delivery_status", "average_review_score"]
].set_index("delivery_status")

st.bar_chart(
    review_chart_df
)