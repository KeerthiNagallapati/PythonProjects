import requests
import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# API Configuration
API_KEY = "a959d52da84b4d94963d5381ef5fbf06"
DEFAULT_STOCK = "AAPL"  # Default stock symbol


# Function to Fetch Stock Data
def fetch_stock_data(symbol):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=365&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "values" not in data:
        return None  # Handle API errors

    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime").astype(float)
    df = df.sort_index()  # Sort by date

    # Calculate Moving Averages
    df["50_MA"] = df["close"].rolling(window=50).mean()
    df["200_MA"] = df["close"].rolling(window=200).mean()

    # Calculate Daily Returns & Volatility
    df["Daily_Return"] = df["close"].pct_change()
    df["Volatility"] = df["Daily_Return"].rolling(window=20).std()

    return df


# Initialize Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📈 Real-Time Stock Market Dashboard", style={'textAlign': 'center'}),

    # Stock Selection Dropdown
    html.Label("Select Stock Symbol:"),
    dcc.Dropdown(
        id='stock-dropdown',
        options=[
            {'label': 'Apple (AAPL)', 'value': 'AAPL'},
            {'label': 'Tesla (TSLA)', 'value': 'TSLA'},
            {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
            {'label': 'Amazon (AMZN)', 'value': 'AMZN'},
            {'label': 'Google (GOOGL)', 'value': 'GOOGL'},
        ],
        value=DEFAULT_STOCK,
        clearable=False
    ),

    dcc.Graph(id='stock-price-chart'),
    dcc.Graph(id='daily-return-chart'),
    dcc.Graph(id='volatility-chart'),

    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # Auto-refresh every 60 seconds
        n_intervals=0
    )
])


# Callback to Update Dashboard
@app.callback(
    [Output('stock-price-chart', 'figure'),
     Output('daily-return-chart', 'figure'),
     Output('volatility-chart', 'figure')],
    [Input('stock-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_dashboard(stock_symbol, n):
    df = fetch_stock_data(stock_symbol)

    if df is None:
        return go.Figure(), go.Figure(), go.Figure()

    # Stock Price Chart
    stock_fig = go.Figure()
    stock_fig.add_trace(go.Scatter(x=df.index, y=df["close"], mode='lines', name="Closing Price"))
    stock_fig.add_trace(go.Scatter(x=df.index, y=df["50_MA"], mode='lines', name="50-Day MA", line=dict(dash='dash')))
    stock_fig.add_trace(go.Scatter(x=df.index, y=df["200_MA"], mode='lines', name="200-Day MA", line=dict(dash='dot')))
    stock_fig.update_layout(title=f"{stock_symbol} Stock Price Trends", xaxis_title="Date",
                            yaxis_title="Stock Price (USD)")

    # Daily Returns Chart
    return_fig = go.Figure()
    return_fig.add_trace(go.Bar(x=df.index, y=df["Daily_Return"], name="Daily Return", marker_color='blue'))
    return_fig.update_layout(title=f"{stock_symbol} Daily Returns", xaxis_title="Date", yaxis_title="Return (%)")

    # Volatility Chart
    volatility_fig = go.Figure()
    volatility_fig.add_trace(
        go.Scatter(x=df.index, y=df["Volatility"], mode='lines', name="Volatility", marker_color='red'))
    volatility_fig.update_layout(title=f"{stock_symbol} Volatility", xaxis_title="Date", yaxis_title="Volatility")

    return stock_fig, return_fig, volatility_fig


# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
