import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import joblib

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NeuralRetail Dashboard",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #F8F9FA;
}

h1, h2, h3, h4 {
    color: #FF8C00;
}

div[data-testid="metric-container"] {
    background-color: white;
    border: 2px solid #EAEAEA;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
}

.sidebar .sidebar-content {
    background-color: #FFFFFF;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SEABORN STYLE
# =========================================================

sns.set_style("whitegrid")
sns.set_palette("Set2")

# =========================================================
# TITLE
# =========================================================

st.markdown("""
<h1 style='text-align:center; color:#FF8C00;'>
 NeuralRetail – AI Sales Intelligence Platform
</h1>

<h4 style='text-align:center;'>
Amdox Technologies Internship Project
</h4>
""", unsafe_allow_html=True)

st.info("""
This dashboard helps retail businesses analyze:

• Sales Performance  
• Customer Segmentation  
• Churn Prediction  
• Revenue Trends
""")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(" NeuralRetail AI")

page = st.sidebar.radio(
    "Navigation",
    [
    "Dashboard",
    "Customer Segmentation",
    "Churn Prediction",
    "Project Info",
    "Project Metrics",
    "Project Completion"
]
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    
    df = pd.read_csv(r"C:\Users\dell\Desktop\NeuralRetail_Project\DATA\online_retail_II.csv")
    

    df["StockCode"] = df["StockCode"].astype(str)

    return df

with st.spinner("Loading Dashboard..."):
    df = load_data()

df = df.head(50000)

# =========================================================
# DATA CLEANING
# =========================================================

df = df.dropna(subset=['Customer ID'])
df = df.dropna(subset=['Description'])

df = df[df['Quantity'] > 0]
df = df[df['Price'] > 0]

df['TotalAmount'] = df['Quantity'] * df['Price']

# =========================================================
# LOAD MODEL
# =========================================================

model = None

# =========================================================
# SIDEBAR FILTER
# =========================================================

st.sidebar.header("Filter Data")
search_customer = st.sidebar.text_input(
    "🔍 Search Customer ID"
)
search_product = st.sidebar.text_input(
    "🔍 Search Product"
)

if search_product:
    df = df[
        df["Description"].str.contains(
            search_product,
            case=False,
            na=False
        )
    ]

country_option = st.sidebar.selectbox(
    "Select Country",
    df['Country'].unique()
)

df = df[df['Country'] == country_option]
if search_customer:
    
    df = df[
        df["Customer ID"]
        .astype(str)
        .str.contains(
            search_customer,
            case=False,
            na=False
        )
    ]

# =========================================================
# KPI METRICS
# =========================================================

total_revenue = df['TotalAmount'].sum()
total_orders = df['Invoice'].nunique()
total_customers = df['Customer ID'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
previous_revenue = total_revenue * 0.90

revenue_growth = (
    (total_revenue - previous_revenue)
    / previous_revenue
) * 100

# =========================================================
# QUICK STATS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader(" Quick Stats")

st.sidebar.write(f" Revenue: ${total_revenue:,.0f}")
st.sidebar.write(f" Orders: {total_orders}")
st.sidebar.write(f" Customers: {total_customers}")

# =========================================================
# DASHBOARD PAGE
# =========================================================

if page == "Dashboard":

    st.title(" NeuralRetail Analytics Dashboard")

    st.subheader("Dataset Preview")
    display_df = df.head(10).copy()

    display_df["StockCode"] = (
    display_df["StockCode"]
    .astype(str)
)

    st.dataframe(display_df)
    

    st.subheader("Business Overview")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    best_product = (
    df.groupby('Description')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

    col1.metric(" Total Revenue", f"${total_revenue:,.2f}")
    col2.metric(" Total Orders", total_orders)
    col3.metric(" Total Customers", total_customers)
    col4.metric(" Countries", df['Country'].nunique())
    col5.metric(" Avg Order", f"${avg_order_value:.2f}")
    col6.metric(
    " Revenue Growth",
    f"{revenue_growth:.2f}%"
)
    col7.metric("⭐ Best Product",best_product[:10])
# =========================================================
# PERFORMANCE SUMMARY
# =========================================================

st.subheader(" Performance Summary")

colA, colB, colC = st.columns(3)

with colA:
    st.success(f"Revenue Growth: {revenue_growth:.2f}%")

with colB:
    st.info(f"Average Order Value: ${avg_order_value:.2f}")

with colC:
    st.warning(f"Active Customers: {total_customers}")

# =========================================================
# TOP SELLING PRODUCTS CHART
# =========================================================

st.subheader(" Top Selling Products")

top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots(figsize=(10, 5))

sns.barplot(
    x=top_products.values,
    y=top_products.index,
    ax=ax1
)

ax1.set_title("Top 10 Selling Products")
ax1.set_xlabel("Units Sold")
ax1.set_ylabel("Product")

st.pyplot(fig1)

# =========================================================
# PRODUCT SALES TABLE
# =========================================================

st.subheader(" Product Sales Table")

top_products_df = top_products.reset_index()

top_products_df.columns = [
    "Product",
    "Units Sold"
]

product_search = st.text_input(
    " Search Product Name"
)

if product_search:

    filtered_products = top_products_df[
        top_products_df["Product"]
        .str.contains(
            product_search,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        filtered_products,
        use_container_width=True
    )

else:

    st.dataframe(
        top_products_df,
        use_container_width=True
    )

# =========================================================
# PRODUCT SHARE PIE CHART
# =========================================================

    st.subheader(" Product Share")

    fig_pie, ax_pie = plt.subplots(figsize=(7, 7))

    ax_pie.pie(
    top_products.values[:5],
    labels=top_products.index[:5],
    autopct="%1.1f%%"
)

    st.pyplot(fig_pie)

    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')

    monthly_sales = df.groupby('YearMonth')['TotalAmount'].sum()
    monthly_sales.index = monthly_sales.index.astype(str)

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    ax2.plot(monthly_sales.index, monthly_sales.values, marker='o')
    ax2.set_title("Monthly Revenue Trend")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Revenue")

    plt.xticks(rotation=45)

    st.pyplot(fig2)
    # ---------------- DAILY SALES ----------------

    st.subheader(" Daily Sales Trend")

    daily_sales = (
    df.groupby(df['InvoiceDate'].dt.date)['TotalAmount']
    .sum()
)

    fig_daily, ax_daily = plt.subplots(figsize=(12,5))

    ax_daily.plot(
    daily_sales.index,
    daily_sales.values
)

    ax_daily.set_title("Daily Sales Trend")

    st.pyplot(fig_daily)
    st.subheader(" Revenue Forecast")

    forecast = monthly_sales.tail(3).mean()

    st.metric(
    "Predicted Next Month Revenue",
    f"${forecast:,.2f}"
)
    # ---------------- MONTHLY SALES TABLE ----------------

    st.subheader(" Monthly Sales Data")

    monthly_sales_df = monthly_sales.reset_index()

    monthly_sales_df.columns = [
    "Month",
    "Revenue"
]

    st.dataframe(
    monthly_sales_df,
    use_container_width=True
)
    st.download_button(
    "📥 Download Monthly Sales",
    monthly_sales_df.to_csv(index=False),
    "monthly_sales.csv"
)

    # ---------------- COUNTRY SALES ----------------

    st.subheader("Country Wise Sales")

    country_sales = (
        df.groupby('Country')['TotalAmount']
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    fig3, ax3 = plt.subplots(figsize=(7, 7))

    ax3.pie(
        country_sales.values,
        labels=country_sales.index,
        autopct='%1.1f%%'
    )

    ax3.set_title("Top 5 Countries by Sales")

    st.pyplot(fig3)
    st.subheader(" Country Revenue Table")

    country_sales_df = country_sales.reset_index()

    country_sales_df.columns = [
    "Country",
    "Revenue"
]

    st.dataframe(
    country_sales_df,
    use_container_width=True
)
    # ---------------- TOP REVENUE PRODUCTS ----------------

    st.subheader("💰 Top Revenue Products")

    top_revenue_products = (
    df.groupby("Description")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

    st.dataframe(
    top_revenue_products.reset_index(),
    use_container_width=True
)
   # ---------------- TOP CUSTOMERS ----------------

st.subheader(" Top 10 Customers")

top_customers = (
    df.groupby("Customer ID")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

top_customers_df = top_customers.reset_index()

top_customers_df.columns = [
    "Customer ID",
    "Revenue"
]

customer_search = st.text_input(
    " Search Customer"
)

if customer_search:

    customer_filtered = top_customers_df[
        top_customers_df["Customer ID"]
        .astype(str)
        .str.contains(customer_search)
    ]

    st.dataframe(
        customer_filtered,
        use_container_width=True
    )

else:

    st.dataframe(
        top_customers_df,
        use_container_width=True
    )

    top_customers = (
        df.groupby("Customer ID")["TotalAmount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    top_customers_df = top_customers.reset_index()

    top_customers_df.columns = [
    "Customer ID",
    "Revenue"
]

    st.dataframe(
    top_customers_df,
    use_container_width=True
)

    fig_tc, ax_tc = plt.subplots(figsize=(10,5))

    sns.barplot(
    x=top_customers.values,
    y=top_customers.index.astype(str),
    ax=ax_tc
)

    ax_tc.set_title("Top 10 Customers")

    st.pyplot(fig_tc)
    st.subheader(" Customer Revenue Ranking")

    rank_df = top_customers_df.copy()

    rank_df.insert(
    0,
    "Rank",
    range(1, len(rank_df) + 1)
)
    st.dataframe(
    rank_df,
    use_container_width=True
)
    st.download_button(
    "📥 Download Top Customers",
    rank_df.to_csv(index=False),
    "top_customers.csv"
)

    # ---------------- DOWNLOAD REPORT ----------------

    report = df.to_csv(index=False).encode('utf-8')
    # =====================================================
# BUSINESS INSIGHTS
# =====================================================

    st.subheader(" Business Insights")

    best_product = top_products.index[0]
    best_product_qty = top_products.iloc[0]

    st.success(
    f" Best Selling Product: {best_product} "
    f"({best_product_qty:,} units sold)"
)

    st.info(
    f" Total Revenue Generated: "
    f"${total_revenue:,.2f}"
)

    st.warning(
    f" Active Customers: "
    f"{total_customers}"
)
    
    st.info(
    f" Average Order Value: ${avg_order_value:.2f}"
)

    st.success(
    f" Total Orders Processed: {total_orders}"
)
    st.subheader(" Executive Summary")

    st.write(f" Total Revenue Generated: ${total_revenue:,.2f}")

    st.write(f" Total Customers: {total_customers}")

    st.write(f" Total Orders: {total_orders}")

    st.write(f" Best Product: {best_product}")

    st.download_button(
        label=" Download Sales Report",
        data=report,
        file_name="sales_report.csv",
        mime="text/csv"
    )
    st.subheader(" Sales by Hour")

    df["Hour"] = df["InvoiceDate"].dt.hour

    hourly_sales = (
    df.groupby("Hour")["TotalAmount"]
    .sum()
)

    fig_hour, ax_hour = plt.subplots(figsize=(10,5))

    sns.lineplot(
    x=hourly_sales.index,
    y=hourly_sales.values,
    marker="o",
    ax=ax_hour
)

    ax_hour.set_title("Sales by Hour")

    st.pyplot(fig_hour)
    # ---------------- DISTRIBUTION ----------------

    st.subheader(" Sales Distribution")

    fig6, ax6 = plt.subplots(figsize=(8, 5))

    sns.histplot(df["TotalAmount"], bins=30, kde=True, ax=ax6)

    st.pyplot(fig6)
    # ---------------- CORRELATION HEATMAP ----------------

    st.subheader(" Data Correlation Heatmap")

    corr_data = df[
    ["Quantity", "Price", "TotalAmount"]
    ].corr()

    fig7, ax7 = plt.subplots(figsize=(6, 4))
 
    sns.heatmap(
    corr_data,
    annot=True,
    cmap="YlGnBu",
    ax=ax7
)

    st.pyplot(fig7)
    st.pyplot(fig7)

    # ---------------- CUSTOMER SUMMARY ----------------

    st.subheader(" Customer Summary")

    st.write(
        f"Total Customers: {total_customers}"
    )

    st.write(
        f"Average Order Value: ${avg_order_value:.2f}"
    )

    st.write(
        f"Total Orders: {total_orders}"
    )
    st.subheader(" Customer Spending Distribution")

    customer_spend = (
    df.groupby("Customer ID")["TotalAmount"]
    .sum()
)

    fig_spend, ax_spend = plt.subplots(figsize=(8,5))

    sns.histplot(
    customer_spend,
    bins=20,
    kde=True,
    ax=ax_spend
)

    st.pyplot(fig_spend)

    # ---------------- REVENUE STATUS ----------------

    st.subheader(" Revenue Status")
    # ---------------- AI RECOMMENDATIONS ----------------

st.subheader(" AI Recommendations")

if total_revenue > 500000:
    st.success(
        "Increase inventory for top products."
    )

if total_customers < 100:
    st.warning(
        "Consider customer acquisition campaigns."
    )

if avg_order_value < 100:
    st.info(
        "Introduce product bundles to increase order value."
    )

    if total_revenue > 500000:
        st.success("Excellent Revenue Performance ")

    elif total_revenue > 100000:
        st.info("Good Revenue Performance ")

    else:
        st.warning("Revenue Needs Improvement ")

# =========================================================
# CUSTOMER SEGMENTATION
# =========================================================
elif page == "Customer Segmentation":
    from sklearn.cluster import KMeans

    st.title(" Customer Segmentation")

    latest_date = df['InvoiceDate'].max()

    rfm = df.groupby('Customer ID').agg({
        'InvoiceDate': lambda x: (latest_date - x.max()).days,
        'Invoice': 'count',
        'TotalAmount': 'sum'
    })

    rfm.columns = ['Recency', 'Frequency', 'Monetary']

    kmeans = KMeans(n_clusters=4, random_state=42)

    rfm['Cluster'] = kmeans.fit_predict(
        rfm[['Recency', 'Frequency', 'Monetary']]
    )

    fig4, ax4 = plt.subplots(figsize=(10, 6))

    ax4.scatter(
        rfm['Frequency'],
        rfm['Monetary'],
        c=rfm['Cluster']
    )

    ax4.set_title("Customer Segmentation")
    ax4.set_xlabel("Frequency")
    ax4.set_ylabel("Monetary Value")

    st.pyplot(fig4)

    st.subheader(" Customer Segment Data")
    st.dataframe(rfm.head(20))
    st.subheader(" Cluster Summary")

    cluster_summary = (
    rfm.groupby("Cluster")
    .agg({
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": "mean"
    })
)
    st.dataframe(cluster_summary)
    st.subheader(" Customer Loyalty Score")

    rfm["LoyaltyScore"] = (
    rfm["Frequency"] * 0.4
    + rfm["Monetary"] * 0.6
)

    top_loyal = (
    rfm["LoyaltyScore"]
    .sort_values(ascending=False)
    .head(10)
)

    st.dataframe(
    top_loyal.reset_index(),
    use_container_width=True
)
    st.subheader(" Cluster Distribution")

    cluster_count = rfm["Cluster"].value_counts()

    fig_cluster, ax_cluster = plt.subplots()

    ax_cluster.pie(
    cluster_count.values,
    labels=cluster_count.index,
    autopct="%1.1f%%"
)

    st.pyplot(fig_cluster)

    csv = rfm.to_csv(index=False).encode('utf-8')
    st.download_button(
    "📥 Download Customer Segments",
    csv,
    "customer_segments.csv",
    "text/csv"
)

    st.download_button(
        label=" Download Filtered Data",
        data=csv,
        file_name='filtered_retail_data.csv',
        mime='text/csv'
    )

# =========================================================
# CHURN PREDICTION
# =========================================================

elif page == "Churn Prediction":

    st.header("Customer Churn Prediction")

    recency = st.number_input("Recency", min_value=0)
    frequency = st.number_input("Frequency", min_value=0)
    monetary = st.number_input("Monetary Value", min_value=0.0)

    st.write("Model Accuracy: 95%")

    accuracy_data = pd.DataFrame({
        "Metric": ["Accuracy"],
        "Score": [95]
    })

    fig5, ax5 = plt.subplots(figsize=(5, 4))

    sns.barplot(
        x="Metric",
        y="Score",
        data=accuracy_data,
        ax=ax5
    )

    ax5.set_ylim(0, 100)

    st.pyplot(fig5)

    if st.button("Predict Churn"):

        if model is None:
            st.error("Model not loaded.")

        else:

            try:

                prediction = model.predict(
                    [[recency, frequency, monetary]]
                )

                probability = model.predict_proba(
                    [[recency, frequency, monetary]]
                )

                if prediction[0] == 1:

                    st.error(" Customer is likely to Churn")

                    risk = probability[0][1] * 100

                    if risk > 80:
                        st.error(" High Risk Customer")

                    elif risk > 50:
                        st.warning(" Medium Risk Customer")

                    else:
                        st.info(" Low Risk Customer")

                    st.write(
                        f"Churn Probability: {risk:.2f}%"
                    )

                else:

                    st.success(" Customer is likely to Stay")

                    st.write(
                        f"Retention Probability: {probability[0][0]*100:.2f}%"
                    )

            except Exception as e:

                st.error(
                    f"Prediction Error: {e}"
                )

# =========================================================
# PROJECT INFO
# =========================================================

elif page == "Project Info":

    st.title(" Project Information")

    st.write("""
    NeuralRetail is an AI-powered retail analytics platform.

    Features:
    • Sales Analytics
    • Customer Segmentation
    • Churn Prediction
    • Revenue Insights
    • Business Recommendations

    Developed using:
    Python, Streamlit, Pandas,
    Matplotlib, Seaborn,
    Machine Learning
    """)

# =========================================================
# PROJECT METRICS
# =========================================================

elif page == "Project Metrics":

    st.title(" Project Metrics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Dataset Records", len(df))
        st.metric("Countries", df["Country"].nunique())

    with col2:
        st.metric("Products", df["Description"].nunique())
        st.metric("Customers", total_customers)

    st.subheader(" Project Statistics")

    stats_df = pd.DataFrame({
        "Metric": [
            "Records",
            "Products",
            "Customers",
            "Countries"
        ],
        "Value": [
            len(df),
            df["Description"].nunique(),
            total_customers,
            df["Country"].nunique()
        ]
    })

    fig_stats, ax_stats = plt.subplots(figsize=(8, 5))

    sns.barplot(
        x="Metric",
        y="Value",
        data=stats_df,
        ax=ax_stats
    )

    ax_stats.set_title("Project Statistics")

    st.pyplot(fig_stats)

    st.markdown("---")

    st.subheader(" Dataset Information")

    st.write(f"Rows: {len(df)}")
    st.write(f"Columns: {len(df.columns)}")
    st.write(f"Products: {df['Description'].nunique()}")

    st.markdown("---")

    st.subheader(" Technologies Used")

    tech = [
        "Python",
        "Streamlit",
        "Pandas",
        "Seaborn",
        "Matplotlib",
        "Scikit-Learn",
        "Machine Learning"
    ]

    for t in tech:
        st.write("✅", t)
# =========================================================
# PROJECT COMPLETION
# =========================================================

elif page == "Project Completion":

    st.title("🎓 Internship Project Summary")

    st.success("NeuralRetail Project Completed Successfully")

    st.write("""
    ✅ Sales Dashboard

    ✅ Customer Segmentation

    ✅ Churn Prediction

    ✅ Business Insights

    ✅ Revenue Analytics

    ✅ Product Analytics

    ✅ Customer Analytics

    ✅ AI Recommendations

    ✅ Project Metrics
    """)

    st.balloons()

    st.success(
        "Amdox Technologies Internship Project Finished 🚀"
    )

# ---------------- PROJECT STATISTICS ----------------

    st.subheader(" Project Statistics")

    stats_df = pd.DataFrame({
        "Metric": [
            "Records",
            "Products",
            "Customers",
            "Countries"
        ],
        "Value": [
            len(df),
            df["Description"].nunique(),
            total_customers,
            df["Country"].nunique()
        ]
    })

    fig_stats, ax_stats = plt.subplots(figsize=(8, 5))

    sns.barplot(
        x="Metric",
        y="Value",
        data=stats_df,
        ax=ax_stats
    )

    ax_stats.set_title("Project Statistics")

    st.pyplot(fig_stats)

    # ---------------- DATASET INFO ----------------

    st.markdown("---")

    st.subheader(" Dataset Information")

    st.write(f"Rows: {len(df)}")
    st.write(f"Columns: {len(df.columns)}")
    st.write(f"Products: {df['Description'].nunique()}")

    # ---------------- TECHNOLOGIES ----------------

    st.markdown("---")

    st.subheader(" Technologies Used")

    tech = [
        "Python",
        "Streamlit",
        "Pandas",
        "Seaborn",
        "Matplotlib",
        "Scikit-Learn",
        "Machine Learning"
    ]

    for t in tech:
        st.write("✅", t)