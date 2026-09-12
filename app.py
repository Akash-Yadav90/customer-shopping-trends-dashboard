import pandas as pd

# Load dataset
df = pd.read_csv("shopping_trends.csv")

# Basic information
print("Dataset Shape:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Information:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


import pandas as pd

# Load dataset
df = pd.read_csv("shopping_trends.csv")

# Remove duplicate rows
df = df.drop_duplicates()

# Check missing values
print("Missing values before cleaning:")
print(df.isnull().sum())

# Fill missing numerical values with median
numeric_columns = df.select_dtypes(include="number").columns

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

# Fill missing categorical values with mode
categorical_columns = df.select_dtypes(include="object").columns

for column in categorical_columns:
    df[column] = df[column].fillna(df[column].mode()[0])

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nFinal Dataset Shape:")
print(df.shape)

#BAR CHART
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("shopping_trends.csv")

# Remove duplicates
df = df.drop_duplicates()

# Category-wise purchase amount
category_sales = (
    df.groupby("Category")["Purchase Amount (USD)"]
    .sum()
    .reset_index()
)

print(category_sales)

# Create bar chart
fig = px.bar(
    category_sales,
    x="Category",
    y="Purchase Amount (USD)",
    title="Total Purchase Amount by Category",
    text_auto=True
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Product Category",
    yaxis_title="Total Purchase Amount (USD)"
)

fig.show()

#LINE CHART
season_order = ["Spring", "Summer", "Fall", "Winter"]

season_sales = (
    df.groupby("Season")["Purchase Amount (USD)"]
    .sum()
    .reindex(season_order)
    .reset_index()
)

fig2 = px.line(
    season_sales,
    x="Season",
    y="Purchase Amount (USD)",
    markers=True,
    title="Purchase Amount Across Seasons"
)

fig2.update_layout(
    template="plotly_white",
    xaxis_title="Season",
    yaxis_title="Total Purchase Amount (USD)"
)

fig2.show()


#SCATTER PLOT
fig3 = px.scatter(
    df,
    x="Age",
    y="Purchase Amount (USD)",
    color="Category",
    hover_data=[
        "Gender",
        "Item Purchased",
        "Subscription Status",
        "Discount Applied"
    ],
    title="Age vs Purchase Amount"
)

fig3.update_layout(
    template="plotly_white",
    xaxis_title="Customer Age",
    yaxis_title="Purchase Amount (USD)"
)

fig3.show()


#HISTOGRAM
fig4 = px.histogram(
    df,
    x="Purchase Amount (USD)",
    nbins=30,
    title="Distribution of Purchase Amount"
)

fig4.update_layout(
    template="plotly_white",
    xaxis_title="Purchase Amount (USD)",
    yaxis_title="Number of Customers"
)

fig4.show()


#HEATMAP
numeric_columns = [
    "Age",
    "Purchase Amount (USD)",
    "Review Rating",
    "Previous Purchases"
]

correlation = df[numeric_columns].corr()

fig5 = px.imshow(
    correlation,
    text_auto=".2f",
    title="Correlation Between Customer Variables",
    aspect="auto"
)

fig5.show()

#BOX PLOT
fig6 = px.box(
    df,
    x="Category",
    y="Purchase Amount (USD)",
    color="Category",
    title="Purchase Amount Distribution by Category"
)

fig6.update_layout(
    template="plotly_white",
    xaxis_title="Product Category",
    yaxis_title="Purchase Amount (USD)"
)

fig6.show()