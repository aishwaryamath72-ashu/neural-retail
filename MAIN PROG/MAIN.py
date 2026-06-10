import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("DATA/online_retail_II.csv")

# -----------------------------
# DATA CLEANING
# -----------------------------

df = df.dropna(subset=['Customer ID'])
df = df.dropna(subset=['Description'])
df = df[df['Quantity'] > 0]
df = df[df['Price'] > 0]

# Create TotalAmount column
df['TotalAmount'] = df['Quantity'] * df['Price']

# -----------------------------
# TOP 10 PRODUCTS
# -----------------------------

top_products = (
    df.groupby('Description')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# -----------------------------
# TOP PRODUCTS BAR CHART
# -----------------------------

plt.figure(figsize=(12,6))

sns.barplot(
    x=top_products.values,
    y=top_products.index
)

plt.title("Top 10 Selling Products")
plt.xlabel("Quantity Sold")
plt.ylabel("Products")

plt.show()

# -----------------------------
# MONTHLY SALES TREND
# -----------------------------

# Create YearMonth column
df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')

monthly_sales = (
    df.groupby('YearMonth')['TotalAmount']
    .sum()
)

# Convert period to string
monthly_sales.index = monthly_sales.index.astype(str)

# -----------------------------
# LINE CHART
# -----------------------------

plt.figure(figsize=(14,6))

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker='o'
)
# -----------------------------
# RFM ANALYSIS
# -----------------------------

import datetime as dt

# Latest date in dataset
latest_date = df['InvoiceDate'].max()

# Create RFM Table
rfm = df.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (latest_date - x.max()).days,
    'Invoice': 'count',
    'TotalAmount': 'sum'
})

# Rename columns
rfm.columns = ['Recency', 'Frequency', 'Monetary']

# -----------------------------
# KMEANS CLUSTERING
# -----------------------------

from sklearn.cluster import KMeans

# Select features
rfm_data = rfm[['Recency', 'Frequency', 'Monetary']]

# Create model
kmeans = KMeans(n_clusters=4, random_state=42)

# Fit model
rfm['Cluster'] = kmeans.fit_predict(rfm_data)

# Display clusters
print("\nCUSTOMER SEGMENTS")
print(rfm.head())

# Display first rows
print("\nRFM ANALYSIS")
print(rfm.head())

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.xticks(rotation=45)

plt.show()
plt.close()
# -----------------------------
# CHURN PREDICTION
# -----------------------------

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Create churn label
rfm['Churn'] = rfm['Recency'].apply(
    lambda x: 1 if x > 90 else 0
)

# Features
X = rfm[['Recency', 'Frequency', 'Monetary']]

# Target
y = rfm['Churn']

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = RandomForestClassifier(random_state=42)

# Train
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nCHURN MODEL ACCURACY")
print(accuracy)

# Confusion Matrix
print("\nCONFUSION MATRIX")
print(confusion_matrix(y_test, y_pred))

# Classification Report
print("\nCLASSIFICATION REPORT")
print(classification_report(y_test, y_pred))
# -----------------------------
# SAVE MODEL
# -----------------------------

import joblib

# Save model
joblib.dump(model, "churn_model.pkl")

print("\nMODEL SAVED SUCCESSFULLY")
# -----------------------------
# SAVE MODEL
# -----------------------------

import joblib

joblib.dump(model, "churn_model.pkl")

print("Model Saved Successfully")
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Dummy training data
X = [[1,2],[2,3],[3,4],[4,5]]
y = [0,1,0,1]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "model/churn_model.pkl")

print("Model saved successfully!")