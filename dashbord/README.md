# NeuralRetail – AI Sales Intelligence Dashboard

## Project Overview
NeuralRetail is an AI-powered retail analytics platform developed using Machine Learning and Streamlit.  
The project helps businesses analyze sales performance, understand customer behavior, segment customers, and predict customer churn.

---

## Features

- Sales Analytics Dashboard
- Customer Segmentation using KMeans Clustering
- Customer Churn Prediction using Random Forest
- Interactive Visualizations
- Country-wise Sales Filtering
- Download Filtered Data Option

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Streamlit
- Joblib

---

## Dataset

Online Retail II Dataset

Dataset contains:
- Customer Transactions
- Product Details
- Invoice Information
- Country-wise Sales Data
python -m streamlit run "dashbord p/dashbord.py"
---

## Machine Learning Models

### Customer Segmentation
Algorithm Used:
- KMeans Clustering

Features:
- Recency
- Frequency
- Monetary Value

### Churn Prediction
Algorithm Used:
- Random Forest Classifier

Target:
- Predict whether customer will churn or stay

---

## Project Structure

```txt
NeuralRetail_Project/
│
├── data/
│   └── online_retail_II.xlsx
│
├── model/
│   └── churn_model.pkl
│
├── MAIN.py
├── dashbord.py
├── requirements.txt
└── README.md