import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv("shopping_trends.csv")

app = Dash(__name__)
app.title = "Customer Shopping Trends Dashboard"

app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "backgroundColor": "#f4f6f8",
        "padding": "25px"
    },
    children=[
        html.H1(
            "Customer Shopping Trends Dashboard",
            style={
                "textAlign": "center",
                "marginBottom": "5px"
            }
        ),

        html.P(
            "What factors influence customer purchasing behavior?",
            style={
                "textAlign": "center",
                "fontSize": "18px",
                "color": "#555"
            }
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",
                "gap": "15px",
                "marginTop": "25px",
                "marginBottom": "25px"
            },
            children=[
                html.Div([
                    html.Label("Category"),
                    dcc.Dropdown(
                        id="category-filter",
                        options=[
                            {"label": "All", "value": "All"}
                        ] + [
                            {"label": x, "value": x}
                            for x in sorted(df["Category"].unique())
                        ],
                        value="All",
                        clearable=False
                    )
                ]),

                html.Div([
                    html.Label("Gender"),
                    dcc.Dropdown(
                        id="gender-filter",
                        options=[
                            {"label": "All", "value": "All"}
                        ] + [
                            {"label": x, "value": x}
                            for x in sorted(df["Gender"].unique())
                        ],
                        value="All",
                        clearable=False
                    )
                ]),

                html.Div([
                    html.Label("Subscription"),
                    dcc.Dropdown(
                        id="subscription-filter",
                        options=[
                            {"label": "All", "value": "All"}
                        ] + [
                            {"label": x, "value": x}
                            for x in sorted(df["Subscription Status"].unique())
                        ],
                        value="All",
                        clearable=False
                    )
                ]),

                html.Div([
                    html.Label("Discount"),
                    dcc.Dropdown(
                        id="discount-filter",
                        options=[
                            {"label": "All", "value": "All"}
                        ] + [
                            {"label": x, "value": x}
                            for x in sorted(df["Discount Applied"].unique())
                        ],
                        value="All",
                        clearable=False
                    )
                ])
            ]
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",
                "gap": "15px",
                "marginBottom": "25px"
            },
            children=[
                html.Div([
                    html.H4("Total Customers"),
                    html.H2(id="total-customers")
                ], style={
                    "backgroundColor": "white",
                    "padding": "20px",
                    "textAlign": "center",
                    "borderRadius": "10px"
                }),

                html.Div([
                    html.H4("Average Purchase"),
                    html.H2(id="average-purchase")
                ], style={
                    "backgroundColor": "white",
                    "padding": "20px",
                    "textAlign": "center",
                    "borderRadius": "10px"
                }),

                html.Div([
                    html.H4("Average Rating"),
                    html.H2(id="average-rating")
                ], style={
                    "backgroundColor": "white",
                    "padding": "20px",
                    "textAlign": "center",
                    "borderRadius": "10px"
                }),

                html.Div([
                    html.H4("Previous Purchases"),
                    html.H2(id="previous-purchases")
                ], style={
                    "backgroundColor": "white",
                    "padding": "20px",
                    "textAlign": "center",
                    "borderRadius": "10px"
                })
            ]
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "20px"
            },
            children=[
                dcc.Graph(id="bar-chart"),
                dcc.Graph(id="line-chart")
            ]
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "20px"
            },
            children=[
                dcc.Graph(id="scatter-chart"),
                dcc.Graph(id="histogram-chart")
            ]
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "20px"
            },
            children=[
                dcc.Graph(id="heatmap-chart"),
                dcc.Graph(id="box-chart")
            ]
        ),

        html.Hr(),

        html.P(
            "Customer Shopping Trends Analysis | Built using Python, Pandas, Plotly and Dash",
            style={
                "textAlign": "center",
                "color": "#666"
            }
        )
    ]
)

@app.callback(
    [
        Output("total-customers", "children"),
        Output("average-purchase", "children"),
        Output("average-rating", "children"),
        Output("previous-purchases", "children"),
        Output("bar-chart", "figure"),
        Output("line-chart", "figure"),
        Output("scatter-chart", "figure"),
        Output("histogram-chart", "figure"),
        Output("heatmap-chart", "figure"),
        Output("box-chart", "figure")
    ],
    [
        Input("category-filter", "value"),
        Input("gender-filter", "value"),
        Input("subscription-filter", "value"),
        Input("discount-filter", "value")
    ]
)
def update_dashboard(
    selected_category,
    selected_gender,
    selected_subscription,
    selected_discount
):
    filtered_df = df.copy()

    if selected_category != "All":
        filtered_df = filtered_df[
            filtered_df["Category"] == selected_category
        ]

    if selected_gender != "All":
        filtered_df = filtered_df[
            filtered_df["Gender"] == selected_gender
        ]

    if selected_subscription != "All":
        filtered_df = filtered_df[
            filtered_df["Subscription Status"] == selected_subscription
        ]

    if selected_discount != "All":
        filtered_df = filtered_df[
            filtered_df["Discount Applied"] == selected_discount
        ]

    total_customers = len(filtered_df)

    average_purchase = (
        filtered_df["Purchase Amount (USD)"].mean()
        if len(filtered_df) > 0 else 0
    )

    average_rating = (
        filtered_df["Review Rating"].mean()
        if len(filtered_df) > 0 else 0
    )

    previous_purchases = (
        filtered_df["Previous Purchases"].mean()
        if len(filtered_df) > 0 else 0
    )

    category_sales = (
        filtered_df
        .groupby("Category")["Purchase Amount (USD)"]
        .sum()
        .reset_index()
    )

    bar_fig = px.bar(
        category_sales,
        x="Category",
        y="Purchase Amount (USD)",
        title="Total Purchase Amount by Category",
        text_auto=True
    )

    bar_fig.update_layout(template="plotly_white")

    season_order = [
        "Spring",
        "Summer",
        "Fall",
        "Winter"
    ]

    season_sales = (
        filtered_df
        .groupby("Season")["Purchase Amount (USD)"]
        .sum()
        .reindex(season_order)
        .reset_index()
    )

    line_fig = px.line(
        season_sales,
        x="Season",
        y="Purchase Amount (USD)",
        markers=True,
        title="Purchase Amount Across Seasons"
    )

    line_fig.update_layout(template="plotly_white")

    scatter_fig = px.scatter(
        filtered_df,
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

    scatter_fig.update_layout(template="plotly_white")

    histogram_fig = px.histogram(
        filtered_df,
        x="Purchase Amount (USD)",
        nbins=30,
        title="Distribution of Purchase Amount"
    )

    histogram_fig.update_layout(template="plotly_white")

    numeric_columns = [
        "Age",
        "Purchase Amount (USD)",
        "Review Rating",
        "Previous Purchases"
    ]

    correlation = filtered_df[numeric_columns].corr()

    heatmap_fig = px.imshow(
        correlation,
        text_auto=".2f",
        title="Correlation Between Customer Variables",
        aspect="auto"
    )

    heatmap_fig.update_layout(template="plotly_white")

    box_fig = px.box(
        filtered_df,
        x="Category",
        y="Purchase Amount (USD)",
        color="Category",
        title="Purchase Amount Distribution by Category"
    )

    box_fig.update_layout(template="plotly_white")

    return (
        f"{total_customers:,}",
        f"${average_purchase:.2f}",
        f"{average_rating:.2f}",
        f"{previous_purchases:.2f}",
        bar_fig,
        line_fig,
        scatter_fig,
        histogram_fig,
        heatmap_fig,
        box_fig
    )
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False) 
