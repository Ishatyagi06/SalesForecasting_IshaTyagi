import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
<style>

/* Main Background */
.stApp{
    background: linear-gradient(135deg,#E3F2FD,#F8F9FA,#E8F5E9);
}

/* Title */
.main-title{
    font-size:42px;
    font-weight:bold;
    text-align:center;
    color:#0D47A1;
}

/* Subtitle */
.sub-title{
    font-size:18px;
    text-align:center;
    color:#555555;
}

/* Cards */
.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.15);
    margin-top:15px;
}

/* Metric Boxes */
.metric-box{
    background:linear-gradient(90deg,#42A5F5,#7E57C2);
    color:white;
    padding:20px;
    border-radius:15px;
    text-align:center;
    font-size:22px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------

st.markdown(
    "<h1 class='main-title'>📊 Sales Forecasting & Demand Intelligence System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>Interactive Dashboard using Streamlit</p>",
    unsafe_allow_html=True
)

# -------------------------
# Load Data
# -------------------------

df = pd.read_csv("train.csv")

# -------------------------
# Metrics
# -------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"<div class='metric-box'>Rows<br>{df.shape[0]}</div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"<div class='metric-box'>Columns<br>{df.shape[1]}</div>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"<div class='metric-box'>Total Sales<br>${df['Sales'].sum():,.0f}</div>",
        unsafe_allow_html=True
    )

# -------------------------
# Dataset Preview
# -------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    "<div class='card'><h3>📋 Dataset Preview</h3></div>",
    unsafe_allow_html=True
)

st.dataframe(df.head(), use_container_width=True)

# ===============================
# Sidebar
# ===============================

with st.sidebar:

    st.markdown(
        """
        <h1 style='text-align:center;color:#1565C0;'>
        📊 Sales Forecasting
        </h1>

        <p style='text-align:center;color:gray;font-size:15px;'>
        Demand Intelligence Dashboard
        </p>

        <hr>
        """,
        unsafe_allow_html=True
    )

    page = st.selectbox(
        "📌 Select Dashboard",
        (
            "🏠 Sales Overview",
            "📈 Forecast Explorer",
            "⚠️ Anomaly Report",
            "📦 Product Segments"
        )
    )

    st.markdown("---")

    st.subheader("📑 Project")

    st.info("""
**Project**

Sales Forecasting &
Demand Intelligence System

Built using:

• Streamlit

• XGBoost

• Prophet

• SARIMA

• Isolation Forest

• K-Means Clustering
""")

    st.markdown("---")

    st.success("✅ Best Model : XGBoost")

    st.caption("Developed by")
    st.write("**Isha Tyagi**")

# ===============================
# PAGE 1 : SALES OVERVIEW
# ===============================

if page == "🏠 Sales Overview":

    st.header("🏠 Sales Overview Dashboard")

    # Convert Date
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)

    # Create Year Column
    df["Year"] = df["Order Date"].dt.year

    # Import Plotly
    import plotly.express as px

    # -----------------------------
    # Total Sales by Year
    # -----------------------------
    sales_year = (
        df.groupby("Year")["Sales"]
          .sum()
          .reset_index()
    )

    fig = px.bar(
        sales_year,
        x="Year",
        y="Sales",
        color="Sales",
        title="📊 Total Sales by Year",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Monthly Sales Trend
    # -----------------------------
    monthly = (
        df.set_index("Order Date")
          .resample("ME")["Sales"]     # <-- Changed M to ME
          .sum()
          .reset_index()
    )

    fig2 = px.line(
        monthly,
        x="Order Date",
        y="Sales",
        markers=True,
        title="📈 Monthly Sales Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # Filters
    # -----------------------------
    st.subheader("🎯 Sales by Region & Category")

    col1, col2 = st.columns(2)

    with col1:
        region = st.selectbox(
            "Select Region",
            ["All"] + sorted(df["Region"].unique())
        )

    with col2:
        category = st.selectbox(
            "Select Category",
            ["All"] + sorted(df["Category"].unique())
        )

    filtered = df.copy()

    if region != "All":
        filtered = filtered[
            filtered["Region"] == region
        ]

    if category != "All":
        filtered = filtered[
            filtered["Category"] == category
        ]

    sales_filtered = (
        filtered.groupby(["Category", "Region"])["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.bar(
        sales_filtered,
        x="Category",
        y="Sales",
        color="Region",
        barmode="group",
        title="📦 Sales by Region & Category"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # =====================================================
# PAGE 2 : FORECAST EXPLORER
# =====================================================

elif page == "📈 Forecast Explorer":

    st.header("📈 Forecast Explorer")

    option = st.selectbox(
        "Select Category / Region",
        [
            "Furniture",
            "Technology",
            "Office Supplies",
            "West",
            "East"
        ]
    )

    horizon = st.slider(
        "Forecast Horizon (Months)",
        min_value=1,
        max_value=3,
        value=3
    )

    forecasts = {
        "Furniture":[14852.28,31729.33,33880.67],
        "Technology":[24482.62,26889.65,22491.69],
        "Office Supplies":[26063.48,33055.79,37447.04],
        "West":[24250.92,26857.66,30180.67],
        "East":[20987.69,24074.96,27955.65]
    }

    months = [
        "October 2018",
        "November 2018",
        "December 2018"
    ]

    chart = pd.DataFrame({
        "Month": months[:horizon],
        "Forecast Sales": forecasts[option][:horizon]
    })

    import plotly.express as px

    fig = px.line(
        chart,
        x="Month",
        y="Forecast Sales",
        markers=True,
        title=f"{option} Forecast"
    )

    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)

    with col1:
        st.metric(
            "MAE",
            "16,989.80"
        )

    with col2:
        st.metric(
            "RMSE",
            "19,665.69"
        )

    st.dataframe(chart, use_container_width=True)

   # ==========================================================
# PAGE 3 : ANOMALY REPORT
# ==========================================================

elif page == "⚠️ Anomaly Report":

    st.header("⚠️ Sales Anomaly Report")

    st.write(
        "Weekly sales anomalies detected using Isolation Forest."
    )


    # ===============================
    # Anomaly Data
    # ===============================

    anomaly_df = pd.DataFrame({

        "Date": [
            "2015-01-04",
            "2015-02-08",
            "2015-02-22",
            "2015-03-22",
            "2015-07-19",
            "2015-09-13",
            "2016-01-24",
            "2017-12-17",
            "2018-11-04",
            "2018-11-18",
            "2018-12-02"
        ],

        "Sales": [
            304.508,
            968.534,
            224.912,
            37703.665,
            1387.686,
            29959.137,
            358.522,
            25449.800,
            29017.467,
            30572.447,
            35998.900
        ]
    })


    # Convert Date column

    anomaly_df["Date"] = pd.to_datetime(
        anomaly_df["Date"]
    )


    # ===============================
    # Anomaly Visualization
    # ===============================

    fig = px.scatter(

        anomaly_df,

        x="Date",

        y="Sales",

        color="Sales",

        size="Sales",

        hover_data={
            "Date": True,
            "Sales": ":,.2f"
        },

        title="Detected Sales Anomalies"

    )


    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        height=500
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ===============================
    # Anomaly Table
    # ===============================

    st.subheader(
        "📋 Detected Anomalies"
    )


    st.dataframe(
        anomaly_df,
        use_container_width=True
    )


    # ===============================
    # KPI
    # ===============================

    st.metric(
        "Total Anomalies Detected",
        len(anomaly_df)
    )


    # ===============================
    # Business Explanation
    # ===============================

    st.info(
    """
    Possible Reasons Behind Anomalies:

    • Holiday or festive season sales spikes

    • Flash discounts and promotional campaigns

    • Stock shortages causing unusual patterns

    • Supply chain disruptions

    • Unexpected customer demand

    """
    )

 # ==========================================================
# PAGE 4 : PRODUCT SEGMENTS
# ==========================================================

elif page == "📦 Product Segments":

    st.header("📦 Product Segmentation Analysis")

    st.write(
        """
        Products are grouped into different segments based on
        sales performance and contribution.
        """
    )


    # ==========================================
    # Product Segment Dataset
    # ==========================================

    segment_df = pd.DataFrame({

        "Product": [
            "Product A",
            "Product B",
            "Product C",
            "Product D",
            "Product E",
            "Product F",
            "Product G",
            "Product H"
        ],

        "Category": [
            "Technology",
            "Furniture",
            "Office Supplies",
            "Technology",
            "Furniture",
            "Office Supplies",
            "Technology",
            "Furniture"
        ],

        "Sales": [
            85000,
            42000,
            18000,
            92000,
            35000,
            12000,
            76000,
            28000
        ],

        "Profit": [
            15000,
            8000,
            3000,
            19000,
            6500,
            2000,
            14000,
            5000
        ]

    })


    # ==========================================
    # Create Product Segments
    # ==========================================

    avg_sales = segment_df["Sales"].mean()


    segment_df["Segment"] = segment_df["Sales"].apply(

        lambda x:

        "High Value"
        if x > avg_sales * 1.5

        else

        "Medium Value"
        if x > avg_sales

        else

        "Low Value"

    )



    # ==========================================
    # KPI Cards
    # ==========================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Total Products",
            len(segment_df)
        )


    with col2:

        high_value = (
            segment_df[
                segment_df["Segment"]=="High Value"
            ]
            .shape[0]
        )

        st.metric(
            "High Value Products",
            high_value
        )


    with col3:

        total_sales = segment_df["Sales"].sum()

        st.metric(
            "Total Sales",
            f"₹ {total_sales:,}"
        )



    st.divider()



    # ==========================================
    # Segment Distribution
    # ==========================================

    st.subheader(
        "📊 Product Segment Distribution"
    )


    segment_count = (
        segment_df
        .groupby("Segment")
        .size()
        .reset_index(name="Count")
    )


    fig1 = px.pie(

        segment_count,

        values="Count",

        names="Segment",

        title="Products by Segment"

    )


    st.plotly_chart(
        fig1,
        use_container_width=True
    )



    # ==========================================
    # Sales Contribution
    # ==========================================

    st.subheader(
        "💰 Sales Contribution by Segment"
    )


    sales_segment = (
        segment_df
        .groupby("Segment")
        ["Sales"]
        .sum()
        .reset_index()
    )


    fig2 = px.bar(

        sales_segment,

        x="Segment",

        y="Sales",

        title="Revenue Contribution"

    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )



    # ==========================================
    # Product Scatter Analysis
    # ==========================================

    st.subheader(
        "🔍 Product Performance Map"
    )


    fig3 = px.scatter(

        segment_df,

        x="Sales",

        y="Profit",

        size="Sales",

        color="Segment",

        hover_name="Product",

        title="Product Segmentation based on Sales & Profit"

    )


    st.plotly_chart(
        fig3,

        use_container_width=True
    )



    # ==========================================
    # Table
    # ==========================================

    st.subheader(
        "📋 Product Segment Details"
    )


    st.dataframe(
        segment_df,
        use_container_width=True
    )



    # ==========================================
    # Insights
    # ==========================================

    st.subheader(
        "💡 Business Insights"
    )


    st.info(
    """
    • High Value products should receive priority in inventory planning.

    • Medium Value products have growth potential.

    • Low Value products should be analyzed for pricing or promotion strategies.

    • Segmentation helps businesses make product-level decisions.
    """
    )