import requests
from dotenv import load_dotenv
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# Step 1: Load environment variables from .env file
load_dotenv()

# Fetch the API key from environment variables
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

BASE_URL = "https://www.alphavantage.co/query"

def fetch_market_data(symbol):
    """Fetch market data for the provided stock symbol."""
    params = {
        "function": "TIME_SERIES_DAILY",  # You can change this to other functions like TIME_SERIES_INTRADAY
        "symbol": symbol,
        "apikey": API_KEY
    }
    
    # Making the request to Alpha Vantage API
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error fetching data from API.")
        return None

def plot_stock_trends(data, symbol):
    """Plot stock price trends using Plotly."""
    # Extracting the time series data for plotting
    time_series = data.get('Time Series (Daily)', {})
    dates = list(time_series.keys())

    # Extract the closing, high, low, and opening prices
    close_prices = [float(time_series[date]['4. close']) for date in dates]
    high_prices = [float(time_series[date]['2. high']) for date in dates]
    low_prices = [float(time_series[date]['3. low']) for date in dates]
    open_prices = [float(time_series[date]['1. open']) for date in dates]

    # Create the plot
    fig = make_subplots(rows=1, cols=1)
    
    # Plot the closing prices
    fig.add_trace(
        go.Scatter(x=dates, y=close_prices, mode='lines', name=f'{symbol} Closing Prices'),
        row=1, col=1
    )

    # Plot the high prices
    fig.add_trace(
        go.Scatter(x=dates, y=high_prices, mode='lines', name=f'{symbol} High Prices', line=dict(dash='dot')),
        row=1, col=1
    )

    # Plot the low prices
    fig.add_trace(
        go.Scatter(x=dates, y=low_prices, mode='lines', name=f'{symbol} Low Prices', line=dict(dash='dash')),
        row=1, col=1
    )

    # Plot the opening prices
    fig.add_trace(
        go.Scatter(x=dates, y=open_prices, mode='lines', name=f'{symbol} Opening Prices', line=dict(dash='solid')),
        row=1, col=1
    )

    # Update the layout of the graph
    fig.update_layout(
        title=f"{symbol} Stock Price Trend",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=True,  # Makes the range slider visible
        template="plotly_dark"
    )

    # Show the plot in the Streamlit app
    st.plotly_chart(fig)

# Step 2: Streamlit UI and interactivity
st.title('Stock Price Trends Visualizer')

# User input to get the stock symbol (default: AAPL)
symbol = st.text_input("Enter Stock Symbol", "AAPL")

if symbol:
    # Fetch market data for the entered stock symbol
    market_data = fetch_market_data(symbol)
    if market_data:
        # Plot the stock trends
        plot_stock_trends(market_data, symbol)
    else:
        # Display error if data is not available
        st.error(f"Failed to fetch data for {symbol}.")
